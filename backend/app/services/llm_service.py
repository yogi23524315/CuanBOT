import google.generativeai as genai
from ..config import settings
import json
from typing import Dict, Any

genai.configure(api_key=settings.gemini_api_key)

class LLMService:
    def __init__(self):
        try:
            # Use the correct Gemini model name
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print(f"LLM Service initialized with gemini-1.5-flash")
        except Exception as e:
            print(f"Error initializing LLM Service: {e}")
            self.model = None
    
    def parse_transaction_fallback(self, user_message: str) -> Dict[str, Any]:
        """
        Fallback parsing using regex patterns for common Indonesian transaction patterns
        """
        import re
        
        # Convert to lowercase for easier matching
        text = user_message.lower()
        
        # Check for transaction type patterns
        buy_patterns = ['beli', 'belanja', 'bayar', 'stok', 'restok']
        sell_patterns = ['jual', 'terima', 'dapat', 'pembayaran', 'penjualan']
        debt_patterns = ['hutang', 'pinjam']
        receivable_patterns = ['piutang', 'tagihan']
        
        # Extract amounts - handle both ribu and juta
        ribu_pattern = r'(\d+)\s*(?:ribu|rb)'
        juta_pattern = r'(\d+)\s*(?:juta|jt)'
        
        ribu_amounts = re.findall(ribu_pattern, text)
        juta_amounts = re.findall(juta_pattern, text)
        
        if not ribu_amounts and not juta_amounts:
            return {"error": "Tidak ditemukan jumlah uang"}
        
        # Calculate total
        total = 0
        total += sum(int(amount) * 1000 for amount in ribu_amounts)
        total += sum(int(amount) * 1000000 for amount in juta_amounts)
        
        # Determine transaction type based on context
        transaction_type = "expense"  # default
        category = "Umum"
        
        # Check for income patterns first (more specific)
        if any(pattern in text for pattern in sell_patterns):
            transaction_type = "income"
            category = "Penjualan"
        elif any(pattern in text for pattern in receivable_patterns):
            transaction_type = "receivable"
            category = "Piutang"
        elif any(pattern in text for pattern in debt_patterns):
            transaction_type = "payable"
            category = "Hutang"
        elif any(pattern in text for pattern in buy_patterns):
            transaction_type = "expense"
            if 'stok' in text or 'belanja' in text:
                category = "Pembelian Stok"
            else:
                category = "Pengeluaran"
        
        # Create description
        total_items = len(ribu_amounts) + len(juta_amounts)
        description = f"Transaksi {category.lower()}"
        if total_items > 1:
            description += f" ({total_items} item)"
        
        return {
            "transaction_type": transaction_type,
            "amount": total,
            "category": category,
            "description": description
        }
    
    def parse_transaction(self, user_message: str) -> Dict[str, Any]:
        prompt = f"""
Analisis pesan transaksi berikut dan ekstrak informasi dalam format JSON.

Pesan: "{user_message}"

ATURAN PARSING:
1. Jika ada MULTIPLE item dengan harga berbeda dalam satu konteks belanja, hitung TOTAL semua
2. Identifikasi tipe transaksi:
   - "expense" untuk belanja/beli/bayar/pengeluaran
   - "income" untuk terima/jual/pendapatan
   - "receivable" untuk piutang
   - "payable" untuk hutang
3. Konversi mata uang: ribu/rb = x1000, juta = x1000000
4. Kategori sesuai konteks bisnis
5. Deskripsi singkat dan jelas

CONTOH:
Input: "Beli beras 265rb, gula 126rb, minyak 165rb untuk stok toko"
Output: {{"transaction_type": "expense", "amount": 556000, "category": "Pembelian Stok", "description": "Belanja stok toko: beras, gula, minyak"}}

Input: "Terima pembayaran customer 500rb"  
Output: {{"transaction_type": "income", "amount": 500000, "category": "Penjualan", "description": "Pembayaran dari customer"}}

WAJIB format JSON:
{{
    "transaction_type": "expense",
    "amount": 1134000,
    "category": "Pembelian Stok",
    "description": "Deskripsi singkat"
}}

Jika tidak bisa diparse sebagai transaksi, return: {{"error": "Tidak dapat memahami transaksi"}}
"""
        
        try:
            if not self.model:
                print("LLM model not initialized, using fallback parsing")
                return self.parse_transaction_fallback(user_message)
                
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                print("Empty response from LLM, using fallback parsing")
                return self.parse_transaction_fallback(user_message)
                
            text = response.text.strip()
            
            # Clean up the response
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            # Try to parse JSON
            result = json.loads(text)
            
            # Validate the result
            if "transaction_type" in result and "amount" in result:
                # Ensure amount is a number
                if isinstance(result["amount"], (int, float)) and result["amount"] > 0:
                    return result
                else:
                    print("Invalid amount from LLM, using fallback parsing")
                    return self.parse_transaction_fallback(user_message)
            else:
                print("Incomplete parsing from LLM, using fallback parsing")
                return self.parse_transaction_fallback(user_message)
                
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}, using fallback parsing")
            return self.parse_transaction_fallback(user_message)
        except Exception as e:
            print(f"LLM parsing error: {e}, using fallback parsing")
            return self.parse_transaction_fallback(user_message)
    
    def answer_accounting_question(self, question: str, context: str = "") -> str:
        prompt = f"""
Kamu adalah asisten akunting CuanBOT untuk UMKM Indonesia. Jawab pertanyaan berikut dengan format yang RINGKAS dan MENARIK.

Pertanyaan: {question}
Konteks: {context if context else "Tidak ada konteks khusus"}

ATURAN PENTING:
1. Jawaban maksimal 10-12 baris
2. Gunakan emoji yang relevan (💰 📊 💡 ✅ ⚠️ 📈 dll) untuk membuat menarik
3. JANGAN gunakan markdown formatting (###, **, ---, *, dll)
4. Gunakan bullet points sederhana dengan emoji
5. Bahasa santai tapi profesional
6. Langsung to the point, tidak bertele-tele
7. WAJIB akhiri dengan soft selling CuanBOT (1 kalimat singkat)

Format jawaban:
[Penjelasan singkat dengan emoji]

[Poin-poin penting dengan emoji]

[Soft selling CuanBOT]

Contoh soft selling:
"Gunakan CuanBOT untuk mencatat transaksi kamu dengan mudah! 🤖"
"CuanBOT siap membantu kelola keuangan UMKM kamu! 💼"
"""
        
        try:
            if not self.model:
                return "Maaf, sistem sedang bermasalah. Coba lagi nanti."
                
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                return "Maaf, tidak ada respons dari sistem. Coba lagi."
                
            return response.text
        except Exception as e:
            return f"Maaf, terjadi error: {str(e)}"
    
    def parse_multiple_transactions(self, user_message: str) -> Dict[str, Any]:
        """
        Parse message that might contain multiple transactions
        Returns either single transaction or list of transactions
        """
        prompt = f"""
Analisis pesan berikut dan tentukan apakah ini berisi SATU transaksi atau MULTIPLE transaksi terpisah.

Pesan: "{user_message}"

ATURAN:
1. Jika semua item adalah BELANJA/PEMBELIAN untuk stok toko → SATU transaksi expense dengan total
2. Jika ada campuran pemasukan dan pengeluaran → MULTIPLE transaksi
3. Jika ada transaksi berbeda waktu/konteks → MULTIPLE transaksi

Untuk SATU transaksi, return:
{{
    "type": "single",
    "transaction": {{
        "transaction_type": "expense",
        "amount": total_semua_item,
        "category": "kategori",
        "description": "deskripsi"
    }}
}}

Untuk MULTIPLE transaksi, return:
{{
    "type": "multiple", 
    "transactions": [
        {{"transaction_type": "expense", "amount": 100000, "category": "cat1", "description": "desc1"}},
        {{"transaction_type": "income", "amount": 200000, "category": "cat2", "description": "desc2"}}
    ]
}}

Konversi: ribu/rb = x1000, juta = x1000000
"""
        
        try:
            if not self.model:
                return {"error": "LLM service not initialized"}
                
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                return {"error": "Empty response from LLM"}
                
            text = response.text.strip()
            
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            result = json.loads(text)
            return result
        except json.JSONDecodeError as e:
            return {"error": f"Error JSON parsing: {str(e)}"}
        except Exception as e:
            return {"error": f"Error parsing multiple transactions: {str(e)}"}
    
    def generate_summary(self, transactions_data: Dict[str, Any]) -> str:
        prompt = f"""
Buatkan ringkasan keuangan RINGKAS dan MENARIK berdasarkan data berikut:

{json.dumps(transactions_data, indent=2)}

ATURAN:
1. Maksimal 8-10 baris
2. Gunakan emoji yang relevan (💰 💸 📊 📈 📉 ✅ ⚠️)
3. JANGAN gunakan markdown formatting (###, **, ---, *, dll)
4. Langsung to the point dengan insight praktis
5. Berikan 1-2 rekomendasi singkat
6. Akhiri dengan soft selling CuanBOT (1 kalimat)

Format:
💰 Pemasukan: Rp X
💸 Pengeluaran: Rp X
📊 Saldo: Rp X

[Insight singkat]
[Rekomendasi praktis]

[Soft selling CuanBOT]
"""
        
        try:
            if not self.model:
                return "Maaf, sistem sedang bermasalah. Tidak dapat membuat ringkasan."
                
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                return "Maaf, tidak dapat membuat ringkasan saat ini."
                
            return response.text
        except Exception as e:
            return f"Maaf, tidak dapat membuat ringkasan: {str(e)}"

llm_service = LLMService()
