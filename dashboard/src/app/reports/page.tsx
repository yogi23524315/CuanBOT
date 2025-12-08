'use client'

import { useEffect, useState, useCallback } from 'react'
import { api } from '@/lib/api'
import { FileDown, Filter, ChevronLeft, ChevronRight, Calendar } from 'lucide-react'

interface Transaction {
  id: number
  user_id: number
  username: string | null
  transaction_type: string
  amount: number
  category: string | null
  description: string | null
  transaction_date: string
  is_anomaly: number
}

interface Summary {
  total_income: number
  total_expense: number
  total_receivable: number
  total_payable: number
  net_balance: number
  transaction_count: number
  period_start: string | null
  period_end: string | null
}

interface ReportData {
  transactions: Transaction[]
  summary: Summary
  total_count: number
}

interface Filters {
  transaction_type: string
  category: string
  start_date: string
  end_date: string
  period: string
}

const ITEMS_PER_PAGE = 20

export default function ReportsPage() {
  const [data, setData] = useState<ReportData | null>(null)
  const [loading, setLoading] = useState(true)
  const [categories, setCategories] = useState<string[]>([])
  const [currentPage, setCurrentPage] = useState(1)
  const [filters, setFilters] = useState<Filters>({
    transaction_type: '',
    category: '',
    start_date: '',
    end_date: '',
    period: 'all',
  })
  const [showFilters, setShowFilters] = useState(true)

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      const result = await api.getReportTransactions({
        skip: (currentPage - 1) * ITEMS_PER_PAGE,
        limit: ITEMS_PER_PAGE,
        transaction_type: filters.transaction_type || undefined,
        category: filters.category || undefined,
        start_date: filters.start_date || undefined,
        end_date: filters.end_date || undefined,
      })
      setData(result)
    } catch (error) {
      console.error('Error loading report data:', error)
    } finally {
      setLoading(false)
    }
  }, [currentPage, filters])

  const loadCategories = async () => {
    try {
      const result = await api.getCategories()
      setCategories(result.categories || [])
    } catch (error) {
      console.error('Error loading categories:', error)
    }
  }

  useEffect(() => {
    loadCategories()
  }, [])

  useEffect(() => {
    loadData()
  }, [loadData])

  const handlePeriodChange = (period: string) => {
    const today = new Date()
    let start = ''
    let end = today.toISOString().split('T')[0]

    switch (period) {
      case 'today':
        start = end
        break
      case 'week':
        const weekAgo = new Date(today)
        weekAgo.setDate(today.getDate() - 7)
        start = weekAgo.toISOString().split('T')[0]
        break
      case 'month':
        const monthAgo = new Date(today)
        monthAgo.setMonth(today.getMonth() - 1)
        start = monthAgo.toISOString().split('T')[0]
        break
      case 'all':
        start = ''
        end = ''
        break
    }

    setFilters(prev => ({
      ...prev,
      period,
      start_date: start,
      end_date: end,
    }))
    setCurrentPage(1)
  }

  const handleFilterChange = (key: keyof Filters, value: string) => {
    if (key === 'period') {
      handlePeriodChange(value)
    } else {
      setFilters(prev => ({ ...prev, [key]: value, period: 'custom' }))
      setCurrentPage(1)
    }
  }

  const handleResetFilters = () => {
    setFilters({
      transaction_type: '',
      category: '',
      start_date: '',
      end_date: '',
      period: 'all',
    })
    setCurrentPage(1)
  }

  const handleExportPdf = () => {
    const url = api.getExportPdfUrl({
      transaction_type: filters.transaction_type || undefined,
      category: filters.category || undefined,
      start_date: filters.start_date || undefined,
      end_date: filters.end_date || undefined,
    })
    window.open(url, '_blank')
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0,
    }).format(amount)
  }

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('id-ID', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      income: 'Pemasukan',
      expense: 'Pengeluaran',
      receivable: 'Piutang',
      payable: 'Hutang',
    }
    return labels[type] || type
  }

  const getTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      income: 'bg-green-100 text-green-800',
      expense: 'bg-red-100 text-red-800',
      receivable: 'bg-blue-100 text-blue-800',
      payable: 'bg-orange-100 text-orange-800',
    }
    return colors[type] || 'bg-gray-100 text-gray-800'
  }

  const totalPages = data ? Math.ceil(data.total_count / ITEMS_PER_PAGE) : 0

  return (
    <div className="h-full">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Laporan Transaksi</h1>
              <p className="mt-1 text-sm text-gray-600">Laporan lengkap transaksi keuangan</p>
            </div>
            <button
              onClick={handleExportPdf}
              className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <FileDown className="w-4 h-4" />
              Download PDF
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        {data && (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
            <div className="bg-white rounded-lg shadow p-4">
              <p className="text-xs text-gray-500 mb-1">Total Pemasukan</p>
              <p className="text-lg font-semibold text-green-600">{formatCurrency(data.summary.total_income)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <p className="text-xs text-gray-500 mb-1">Total Pengeluaran</p>
              <p className="text-lg font-semibold text-red-600">{formatCurrency(data.summary.total_expense)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <p className="text-xs text-gray-500 mb-1">Saldo Bersih</p>
              <p className={`text-lg font-semibold ${data.summary.net_balance >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(data.summary.net_balance)}
              </p>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <p className="text-xs text-gray-500 mb-1">Total Piutang</p>
              <p className="text-lg font-semibold text-blue-600">{formatCurrency(data.summary.total_receivable)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <p className="text-xs text-gray-500 mb-1">Total Hutang</p>
              <p className="text-lg font-semibold text-orange-600">{formatCurrency(data.summary.total_payable)}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <p className="text-xs text-gray-500 mb-1">Jumlah Transaksi</p>
              <p className="text-lg font-semibold text-gray-900">{data.summary.transaction_count}</p>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="p-4 border-b flex items-center justify-between">
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center gap-2 text-gray-700 hover:text-gray-900"
            >
              <Filter className="w-4 h-4" />
              <span className="font-medium">Filter</span>
            </button>
            {(filters.transaction_type || filters.category || filters.period !== 'all') && (
              <button
                onClick={handleResetFilters}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                Reset Filter
              </button>
            )}
          </div>
          
          {showFilters && (
            <div className="p-4 space-y-4">
              {/* Period Quick Filters */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Periode</label>
                <div className="flex flex-wrap gap-2">
                  {[
                    { value: 'today', label: 'Hari Ini' },
                    { value: 'week', label: 'Minggu Ini' },
                    { value: 'month', label: 'Bulan Ini' },
                    { value: 'all', label: 'Semua' },
                    { value: 'custom', label: 'Custom' },
                  ].map((period) => (
                    <button
                      key={period.value}
                      onClick={() => handlePeriodChange(period.value)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        filters.period === period.value
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {period.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Detailed Filters */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tipe Transaksi</label>
                  <select
                    value={filters.transaction_type}
                    onChange={(e) => handleFilterChange('transaction_type', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Semua Tipe</option>
                    <option value="income">Pemasukan</option>
                    <option value="expense">Pengeluaran</option>
                    <option value="receivable">Piutang</option>
                    <option value="payable">Hutang</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Kategori</label>
                  <select
                    value={filters.category}
                    onChange={(e) => handleFilterChange('category', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Semua Kategori</option>
                    {categories.map((cat) => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tanggal Mulai</label>
                  <input
                    type="date"
                    value={filters.start_date}
                    onChange={(e) => handleFilterChange('start_date', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tanggal Akhir</label>
                  <input
                    type="date"
                    value={filters.end_date}
                    onChange={(e) => handleFilterChange('end_date', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          {loading ? (
            <div className="p-8 text-center text-gray-500">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p className="mt-2">Loading...</p>
            </div>
          ) : data && data.transactions.length > 0 ? (
            <>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">No</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tanggal</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipe</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kategori</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Deskripsi</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Jumlah</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {data.transactions.map((txn, idx) => (
                      <tr key={txn.id} className={txn.is_anomaly ? 'bg-red-50' : 'hover:bg-gray-50'}>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                          {(currentPage - 1) * ITEMS_PER_PAGE + idx + 1}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                          {formatDate(txn.transaction_date)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getTypeColor(txn.transaction_type)}`}>
                            {getTypeLabel(txn.transaction_type)}
                          </span>
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                          {txn.category || '-'}
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-500 max-w-xs truncate">
                          {txn.description || '-'}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap text-sm text-right font-medium text-gray-900">
                          {formatCurrency(txn.amount)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              <div className="px-4 py-3 border-t flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="text-sm text-gray-500">
                  Menampilkan {(currentPage - 1) * ITEMS_PER_PAGE + 1} - {Math.min(currentPage * ITEMS_PER_PAGE, data.total_count)} dari {data.total_count} transaksi
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                    className="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <ChevronLeft className="w-4 h-4" />
                  </button>
                  <span className="text-sm text-gray-700">
                    Halaman {currentPage} dari {totalPages}
                  </span>
                  <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                    className="p-2 rounded-lg border border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="p-8 text-center text-gray-500">
              <Calendar className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <p className="text-lg font-medium">Tidak ada transaksi ditemukan</p>
              <p className="text-sm mt-1">Coba ubah filter atau periode waktu</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
