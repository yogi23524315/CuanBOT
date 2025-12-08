from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import datetime, timedelta
from io import BytesIO
from ..database import get_db
from ..models.transaction import Transaction, TransactionType
from ..models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/reports", tags=["reports"])

class ReportTransaction(BaseModel):
    id: int
    user_id: int
    username: Optional[str]
    transaction_type: str
    amount: float
    category: Optional[str]
    description: Optional[str]
    transaction_date: datetime
    is_anomaly: int
    
    class Config:
        from_attributes = True

class ReportSummary(BaseModel):
    total_income: float
    total_expense: float
    total_receivable: float
    total_payable: float
    net_balance: float
    transaction_count: int
    period_start: Optional[str]
    period_end: Optional[str]

class ReportResponse(BaseModel):
    transactions: List[ReportTransaction]
    summary: ReportSummary
    total_count: int

@router.get("/transactions", response_model=ReportResponse)
def get_report_transactions(
    skip: int = 0,
    limit: int = 50,
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get transactions for reporting with filters."""
    query = db.query(Transaction, User.username).join(User, Transaction.user_id == User.id)
    
    # Apply filters
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    if category:
        query = query.filter(Transaction.category.ilike(f"%{category}%"))
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(Transaction.transaction_date >= start_dt)
        except:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            # Add 1 day to include the end date
            end_dt = end_dt + timedelta(days=1)
            query = query.filter(Transaction.transaction_date < end_dt)
        except:
            pass
    
    # Get total count
    total_count = query.count()
    
    # Get paginated results
    results = query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()
    
    # Build transactions list
    transactions = []
    for txn, username in results:
        transactions.append(ReportTransaction(
            id=txn.id,
            user_id=txn.user_id,
            username=username,
            transaction_type=txn.transaction_type.value if hasattr(txn.transaction_type, 'value') else txn.transaction_type,
            amount=txn.amount,
            category=txn.category,
            description=txn.description,
            transaction_date=txn.transaction_date,
            is_anomaly=txn.is_anomaly
        ))
    
    # Calculate summary (for all filtered data, not just paginated)
    summary_query = db.query(Transaction)
    if user_id:
        summary_query = summary_query.filter(Transaction.user_id == user_id)
    if transaction_type:
        summary_query = summary_query.filter(Transaction.transaction_type == transaction_type)
    if category:
        summary_query = summary_query.filter(Transaction.category.ilike(f"%{category}%"))
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            summary_query = summary_query.filter(Transaction.transaction_date >= start_dt)
        except:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            end_dt = end_dt + timedelta(days=1)
            summary_query = summary_query.filter(Transaction.transaction_date < end_dt)
        except:
            pass
    
    all_transactions = summary_query.all()
    
    total_income = sum(t.amount for t in all_transactions if t.transaction_type == TransactionType.INCOME)
    total_expense = sum(t.amount for t in all_transactions if t.transaction_type == TransactionType.EXPENSE)
    total_receivable = sum(t.amount for t in all_transactions if t.transaction_type == TransactionType.RECEIVABLE)
    total_payable = sum(t.amount for t in all_transactions if t.transaction_type == TransactionType.PAYABLE)
    
    summary = ReportSummary(
        total_income=total_income,
        total_expense=total_expense,
        total_receivable=total_receivable,
        total_payable=total_payable,
        net_balance=total_income - total_expense,
        transaction_count=len(all_transactions),
        period_start=start_date,
        period_end=end_date
    )
    
    return ReportResponse(
        transactions=transactions,
        summary=summary,
        total_count=total_count
    )

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Get all unique categories."""
    results = db.query(Transaction.category).distinct().filter(Transaction.category.isnot(None)).all()
    return {"categories": [r[0] for r in results if r[0]]}

@router.get("/export/pdf")
def export_pdf(
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Export transactions to PDF report."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    import pytz
    
    # Query transactions
    query = db.query(Transaction, User.username).join(User, Transaction.user_id == User.id)
    
    if user_id:
        query = query.filter(Transaction.user_id == user_id)
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    if category:
        query = query.filter(Transaction.category.ilike(f"%{category}%"))
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(Transaction.transaction_date >= start_dt)
        except:
            pass
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            end_dt = end_dt + timedelta(days=1)
            query = query.filter(Transaction.transaction_date < end_dt)
        except:
            pass
    
    results = query.order_by(Transaction.transaction_date.desc()).all()
    
    # Calculate summary
    total_income = sum(t.amount for t, _ in results if t.transaction_type == TransactionType.INCOME)
    total_expense = sum(t.amount for t, _ in results if t.transaction_type == TransactionType.EXPENSE)
    total_receivable = sum(t.amount for t, _ in results if t.transaction_type == TransactionType.RECEIVABLE)
    total_payable = sum(t.amount for t, _ in results if t.transaction_type == TransactionType.PAYABLE)
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=landscape(A4), 
        rightMargin=1*cm, 
        leftMargin=1*cm, 
        topMargin=1.5*cm, 
        bottomMargin=1.5*cm
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1E40AF'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=5,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    # Title
    elements.append(Paragraph("LAPORAN KEUANGAN CUANBOT", title_style))
    elements.append(Spacer(1, 5))
    
    # Period info
    period_text = "Periode: "
    if start_date and end_date:
        period_text += f"{start_date[:10]} s/d {end_date[:10]}"
    elif start_date:
        period_text += f"Dari {start_date[:10]}"
    elif end_date:
        period_text += f"Sampai {end_date[:10]}"
    else:
        period_text += "Semua Waktu"
    
    # Get current time in Indonesia timezone (WIB)
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    now_jakarta = datetime.now(jakarta_tz)
    
    # Format bulan dalam bahasa Indonesia
    bulan_indonesia = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    
    tanggal_cetak = f"{now_jakarta.day} {bulan_indonesia[now_jakarta.month]} {now_jakarta.year}, {now_jakarta.strftime('%H:%M')} WIB"
    
    elements.append(Paragraph(period_text, subtitle_style))
    elements.append(Paragraph(f"Dicetak: {tanggal_cetak}", subtitle_style))
    elements.append(Spacer(1, 20))
    
    # Summary Section
    elements.append(Paragraph("RINGKASAN KEUANGAN", heading_style))
    
    summary_data = [
        ["Kategori", "Jumlah"],
        ["Total Pemasukan", f"Rp {total_income:,.0f}"],
        ["Total Pengeluaran", f"Rp {total_expense:,.0f}"],
        ["Saldo Bersih", f"Rp {(total_income - total_expense):,.0f}"],
        ["Total Piutang", f"Rp {total_receivable:,.0f}"],
        ["Total Hutang", f"Rp {total_payable:,.0f}"],
        ["Jumlah Transaksi", str(len(results))],
    ]
    
    summary_table = Table(summary_data, colWidths=[8*cm, 6*cm])
    summary_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#1F2937')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        
        # Highlight Saldo Bersih
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#F3F4F6')),
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, 3), (1, 3), 
         colors.HexColor('#059669') if (total_income - total_expense) >= 0 else colors.HexColor('#DC2626')),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 25))
    
    # Transaction Details
    if results:
        elements.append(Paragraph("DETAIL TRANSAKSI", heading_style))
        elements.append(Spacer(1, 10))
        
        table_data = [["No", "Tanggal", "Tipe", "Kategori", "Deskripsi", "Jumlah"]]
        
        for idx, (txn, username) in enumerate(results, 1):
            txn_type = txn.transaction_type.value if hasattr(txn.transaction_type, 'value') else txn.transaction_type
            type_label = {
                'income': '💰 Pemasukan',
                'expense': '💸 Pengeluaran',
                'receivable': '📝 Piutang',
                'payable': '📋 Hutang'
            }.get(txn_type, txn_type)
            
            desc = txn.description or '-'
            if len(desc) > 40:
                desc = desc[:37] + '...'
            
            table_data.append([
                str(idx),
                txn.transaction_date.strftime('%d/%m/%Y\n%H:%M'),
                type_label,
                txn.category or '-',
                desc,
                f"Rp {txn.amount:,.0f}",
            ])
        
        col_widths = [1.2*cm, 2.5*cm, 3*cm, 2.8*cm, 6*cm, 3.5*cm]
        txn_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Build table style
        table_style = [
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (4, -1), 'LEFT'),
            ('ALIGN', (5, 1), (5, -1), 'RIGHT'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]
        
        # Alternating row colors
        for i in range(1, len(table_data)):
            if i % 2 == 0:
                table_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F9FAFB')))
            else:
                table_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))
        
        txn_table.setStyle(TableStyle(table_style))
        elements.append(txn_table)
    else:
        elements.append(Paragraph("Tidak ada transaksi untuk periode ini.", styles['Normal']))
    
    # Footer note
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#9CA3AF'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph(
        "Laporan ini dibuat secara otomatis oleh CuanBot - Akunting Chatbot untuk UMKM Indonesia",
        footer_style
    ))
    
    doc.build(elements)
    buffer.seek(0)
    
    filename = f"laporan_keuangan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
