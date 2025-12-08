const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = {
  // Dashboard Overview
  async getDashboardOverview() {
    const response = await fetch(`${API_BASE_URL}/api/dashboard/overview`)
    if (!response.ok) throw new Error('Failed to fetch dashboard overview')
    return response.json()
  },

  // Transactions
  async getTransactions(params?: {
    skip?: number
    limit?: number
    transaction_type?: string
    user_id?: number
  }) {
    const queryParams = new URLSearchParams()
    if (params?.skip) queryParams.append('skip', params.skip.toString())
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    if (params?.transaction_type) queryParams.append('transaction_type', params.transaction_type)
    if (params?.user_id) queryParams.append('user_id', params.user_id.toString())

    const response = await fetch(`${API_BASE_URL}/api/transactions?${queryParams}`)
    if (!response.ok) throw new Error('Failed to fetch transactions')
    return response.json()
  },

  async getTransactionStats(params?: {
    user_id?: number
    start_date?: string
    end_date?: string
  }) {
    const queryParams = new URLSearchParams()
    if (params?.user_id) queryParams.append('user_id', params.user_id.toString())
    if (params?.start_date) queryParams.append('start_date', params.start_date)
    if (params?.end_date) queryParams.append('end_date', params.end_date)

    const response = await fetch(`${API_BASE_URL}/api/transactions/stats?${queryParams}`)
    if (!response.ok) throw new Error('Failed to fetch transaction stats')
    return response.json()
  },

  async getDailyTransactions(params?: {
    days?: number
    user_id?: number
  }) {
    const queryParams = new URLSearchParams()
    if (params?.days) queryParams.append('days', params.days.toString())
    if (params?.user_id) queryParams.append('user_id', params.user_id.toString())

    const response = await fetch(`${API_BASE_URL}/api/transactions/daily?${queryParams}`)
    if (!response.ok) throw new Error('Failed to fetch daily transactions')
    return response.json()
  },

  async getTransactionsByCategory(params?: {
    user_id?: number
    transaction_type?: string
  }) {
    const queryParams = new URLSearchParams()
    if (params?.user_id) queryParams.append('user_id', params.user_id.toString())
    if (params?.transaction_type) queryParams.append('transaction_type', params.transaction_type)

    const response = await fetch(`${API_BASE_URL}/api/transactions/by-category?${queryParams}`)
    if (!response.ok) throw new Error('Failed to fetch transactions by category')
    return response.json()
  },

  // Predictions
  async generateForecast(data: {
    user_id?: number
    periods?: number
  }) {
    const response = await fetch(`${API_BASE_URL}/api/predictions/forecast`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw new Error('Failed to generate forecast')
    return response.json()
  },

  async detectAnomalies(data: {
    user_id?: number
  }) {
    const response = await fetch(`${API_BASE_URL}/api/predictions/anomaly`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    if (!response.ok) throw new Error('Failed to detect anomalies')
    return response.json()
  },

  async getPredictionHistory(params?: {
    prediction_type?: string
    limit?: number
  }) {
    const queryParams = new URLSearchParams()
    if (params?.prediction_type) queryParams.append('prediction_type', params.prediction_type)
    if (params?.limit) queryParams.append('limit', params.limit.toString())

    const response = await fetch(`${API_BASE_URL}/api/predictions/history?${queryParams}`)
    if (!response.ok) throw new Error('Failed to fetch prediction history')
    return response.json()
  },

  // Bot Logs
  async getBotLogs(params?: {
    skip?: number
    limit?: number
    level?: string
    user_id?: number
  }) {
    const queryParams = new URLSearchParams()
    if (params?.skip) queryParams.append('skip', params.skip.toString())
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    if (params?.level) queryParams.append('level', params.level)
    if (params?.user_id) queryParams.append('user_id', params.user_id.toString())

    const response = await fetch(`${API_BASE_URL}/api/bot-logs?${queryParams}`)
    if (!response.ok) throw new Error('Failed to fetch bot logs')
    return response.json()
  },

  async getBotStats() {
    const response = await fetch(`${API_BASE_URL}/api/bot-logs/stats`)
    if (!response.ok) throw new Error('Failed to fetch bot stats')
    return response.json()
  },

  // Reset Data
  async resetAllTransactions() {
    const response = await fetch(`${API_BASE_URL}/api/transactions/reset?confirm=true`, {
      method: 'DELETE',
    })
    if (!response.ok) throw new Error('Failed to reset transactions')
    return response.json()
  },

  // Generate Sample Data
  async generateSampleData() {
    const response = await fetch(`${API_BASE_URL}/api/transactions/generate-sample`, {
      method: 'POST',
    })
    if (!response.ok) throw new Error('Failed to generate sample data')
    return response.json()
  },

  // Reports
  async getReportTransactions(params?: {
    skip?: number
    limit?: number
    transaction_type?: string
    category?: string
    start_date?: string
    end_date?: string
    user_id?: number
  }) {
    const queryParams = new URLSearchParams()
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString())
    if (params?.limit) queryParams.append('limit', params.limit.toString())
    if (params?.transaction_type) queryParams.append('transaction_type', params.transaction_type)
    if (params?.category) queryParams.append('category', params.category)
    if (params?.start_date) queryParams.append('start_date', params.start_date)
    if (params?.end_date) queryParams.append('end_date', params.end_date)
    if (params?.user_id) queryParams.append('user_id', params.user_id.toString())

    const response = await fetch(`${API_BASE_URL}/api/reports/transactions?${queryParams}`)
    if (!response.ok) throw new Error('Failed to fetch report transactions')
    return response.json()
  },

  async getCategories() {
    const response = await fetch(`${API_BASE_URL}/api/reports/categories`)
    if (!response.ok) throw new Error('Failed to fetch categories')
    return response.json()
  },

  getExportPdfUrl(params?: {
    transaction_type?: string
    category?: string
    start_date?: string
    end_date?: string
    user_id?: number
  }) {
    const queryParams = new URLSearchParams()
    if (params?.transaction_type) queryParams.append('transaction_type', params.transaction_type)
    if (params?.category) queryParams.append('category', params.category)
    if (params?.start_date) queryParams.append('start_date', params.start_date)
    if (params?.end_date) queryParams.append('end_date', params.end_date)
    if (params?.user_id) queryParams.append('user_id', params.user_id.toString())

    return `${API_BASE_URL}/api/reports/export/pdf?${queryParams}`
  },
}
