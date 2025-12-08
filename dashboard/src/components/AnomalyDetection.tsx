'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

interface AnomalyReason {
    type: string
    message: string
    severity: string
}

interface Anomaly {
    transaction_id: number
    amount: number
    transaction_type: string
    category: string
    description: string
    date: string
    anomaly_score: number
    severity: string
    reasons: AnomalyReason[]
}

interface AnomalySummary {
    total_transactions: number
    anomalies_detected: number
    anomaly_types: {
        [key: string]: number
    }
    high_severity: number
    medium_severity: number
    low_severity: number
}

export default function AnomalyDetection() {
    const [anomalies, setAnomalies] = useState<Anomaly[]>([])
    const [summary, setSummary] = useState<AnomalySummary | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const detectAnomalies = async () => {
        setLoading(true)
        setError(null)
        try {
            console.log('Detecting anomalies...')
            const result = await api.detectAnomalies({})
            console.log('Anomaly result:', result)

            if (result.status === 'success') {
                setAnomalies(result.anomalies || [])
                setSummary(result.summary || null)
            } else if (result.status === 'insufficient_data') {
                setError(result.message)
                setAnomalies([])
                setSummary(null)
            } else {
                setError('Failed to detect anomalies')
            }
        } catch (err) {
            console.error('Error detecting anomalies:', err)
            setError('Error detecting anomalies')
        } finally {
            setLoading(false)
        }
    }

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'high':
                return 'bg-red-100 text-red-800 border-red-300'
            case 'medium':
                return 'bg-yellow-100 text-yellow-800 border-yellow-300'
            case 'low':
                return 'bg-blue-100 text-blue-800 border-blue-300'
            default:
                return 'bg-gray-100 text-gray-800 border-gray-300'
        }
    }

    const getSeverityIcon = (severity: string) => {
        switch (severity) {
            case 'high':
                return '🚨'
            case 'medium':
                return '⚠️'
            case 'low':
                return 'ℹ️'
            default:
                return '🔍'
        }
    }

    const getTypeIcon = (type: string) => {
        switch (type) {
            case 'duplicate':
                return '📋'
            case 'large_expense':
                return '💸'
            case 'odd_hours':
                return '🌙'
            case 'unusual_category':
                return '❓'
            case 'frequent_capital':
                return '💰'
            case 'salary_spike':
                return '📈'
            case 'operational_spike':
                return '⚡'
            default:
                return '🔍'
        }
    }

    return (
        <div className="bg-white rounded-lg shadow p-6">
            {/* Header */}
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                        🛑 Anomali Transaksi
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                        Deteksi otomatis transaksi mencurigakan menggunakan Isolation Forest
                    </p>
                </div>
                <button
                    onClick={detectAnomalies}
                    disabled={loading}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400 transition-colors shadow-md hover:shadow-lg font-medium"
                >
                    {loading ? '🔍 Scanning...' : 'Scan Anomali'}
                </button>
            </div>

            {/* Summary Stats */}
            {summary && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 p-4 bg-gray-50 rounded-lg">
                    <div className="text-center">
                        <p className="text-sm text-gray-600">Total Transaksi</p>
                        <p className="text-2xl font-bold text-gray-900">{summary.total_transactions}</p>
                    </div>
                    <div className="text-center">
                        <p className="text-sm text-gray-600">Anomali Terdeteksi</p>
                        <p className="text-2xl font-bold text-red-600">{summary.anomalies_detected}</p>
                    </div>
                    <div className="text-center">
                        <p className="text-sm text-gray-600">Tingkat Tinggi</p>
                        <p className="text-2xl font-bold text-red-600">🚨 {summary.high_severity}</p>
                    </div>
                    <div className="text-center">
                        <p className="text-sm text-gray-600">Tingkat Sedang</p>
                        <p className="text-2xl font-bold text-yellow-600">⚠️ {summary.medium_severity}</p>
                    </div>
                </div>
            )}

            {/* Error Message */}
            {error && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                    <p className="text-yellow-800 text-sm">{error}</p>
                </div>
            )}

            {/* Anomalies List */}
            {anomalies.length === 0 && !loading && !error && (
                <div className="text-center py-12">
                    <p className="text-lg font-medium text-gray-900">Tidak ada anomali terdeteksi</p>
                    <p className="text-sm text-gray-600 mt-2">Klik tombol "Scan Anomali" untuk memulai deteksi</p>
                </div>
            )}

            {anomalies.length > 0 && (
                <div className="max-h-96 overflow-y-auto pr-2 space-y-3">
                    {anomalies.map((anomaly, index) => (
                        <div
                            key={index}
                            className={`border-l-4 rounded-lg p-4 transition-all hover:shadow-md ${anomaly.severity === 'high'
                                ? 'border-red-500 bg-red-50'
                                : anomaly.severity === 'medium'
                                    ? 'border-yellow-500 bg-yellow-50'
                                    : 'border-blue-500 bg-blue-50'
                                }`}
                        >
                            {/* Anomaly Header */}
                            <div className="flex items-start justify-between mb-3">
                                <div className="flex items-center gap-2">
                                    <span className="text-2xl">{getSeverityIcon(anomaly.severity)}</span>
                                    <div>
                                        <p className="font-semibold text-gray-900">
                                            {anomaly.category} - Rp {anomaly.amount.toLocaleString('id-ID')}
                                        </p>
                                        <p className="text-xs text-gray-600">
                                            {new Date(anomaly.date).toLocaleString('id-ID')} • ID: {anomaly.transaction_id}
                                        </p>
                                    </div>
                                </div>
                                <span
                                    className={`px-3 py-1 rounded-full text-xs font-semibold ${anomaly.severity === 'high'
                                        ? 'bg-red-200 text-red-800'
                                        : anomaly.severity === 'medium'
                                            ? 'bg-yellow-200 text-yellow-800'
                                            : 'bg-blue-200 text-blue-800'
                                        }`}
                                >
                                    {anomaly.severity.toUpperCase()}
                                </span>
                            </div>

                            {/* Anomaly Reasons */}
                            <div className="space-y-2">
                                {anomaly.reasons.map((reason, idx) => (
                                    <div
                                        key={idx}
                                        className="flex items-start gap-2 bg-white bg-opacity-60 rounded-md p-3"
                                    >
                                        <span className="text-lg">{getTypeIcon(reason.type)}</span>
                                        <div className="flex-1">
                                            <p className="text-sm font-medium text-gray-900">{reason.message}</p>
                                            {anomaly.description && idx === 0 && (
                                                <p className="text-xs text-gray-600 mt-1">"{anomaly.description}"</p>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Anomaly Score */}
                            <div className="mt-3 pt-3 border-t border-gray-200">
                                <div className="flex items-center justify-between text-xs text-gray-600">
                                    <span>Anomaly Score: {anomaly.anomaly_score.toFixed(4)}</span>
                                    <span className="text-gray-500">
                                        {anomaly.transaction_type === 'expense' ? '📤 Pengeluaran' : '📥 Pemasukan'}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {loading && (
                <div className="text-center py-12">
                    <div className="animate-spin text-6xl mb-4">🔍</div>
                    <p className="text-lg font-medium text-gray-900">Scanning transaksi...</p>
                    <p className="text-sm text-gray-600 mt-2">Menganalisis pola dengan Isolation Forest</p>
                </div>
            )}
        </div>
    )
}
