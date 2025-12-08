'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { X, AlertCircle } from 'lucide-react'

interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const router = useRouter()
  const [mode, setMode] = useState<'login' | 'register'>('register')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 500))

    // Hardcoded credentials
    const VALID_EMAIL = 'hi@cuanbot.id'
    const VALID_PASSWORD = 'cuanbot2025'

    if (email === VALID_EMAIL && password === VALID_PASSWORD) {
      // Login successful
      localStorage.setItem('isAuthenticated', 'true')
      localStorage.setItem('userEmail', email)
      
      // Close modal and redirect to dashboard
      onClose()
      router.push('/')
    } else {
      // Login failed
      if (email !== VALID_EMAIL) {
        setError('Email tidak terdaftar. Silakan periksa kembali email Anda.')
      } else {
        setError('Password salah. Silakan coba lagi.')
      }
      setLoading(false)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    await new Promise(resolve => setTimeout(resolve, 500))

    // For demo, just show success message
    alert('Fitur registrasi akan segera hadir! Untuk demo, gunakan:\nEmail: hi@cuanbot.id\nPassword: cuanbot2025')
    setMode('login')
    setLoading(false)
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              {mode === 'login' ? 'Masuk ke CuanBot' : 'Daftar CuanBot'}
            </h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-red-800">Login Gagal</p>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
            </div>
          )}

          <form onSubmit={mode === 'login' ? handleLogin : handleRegister} className="space-y-4">
            {mode === 'register' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nama Lengkap
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="John Doe"
                />
              </div>
            )}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="email@example.com"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="••••••••"
                required
              />
            </div>
            {mode === 'register' && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nomor Telegram
                  </label>
                  <input
                    type="tel"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="+62812345678"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Pilih Paket
                  </label>
                  <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
                    <option value="personal">Personal - Rp 25.000/bulan</option>
                    <option value="umkm">UMKM - Rp 50.000/bulan</option>
                  </select>
                </div>
              </>
            )}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {loading ? 'Memproses...' : mode === 'login' ? 'Masuk' : 'Daftar Gratis 14 Hari'}
            </button>
            
            {mode === 'login' && (
              <div className="text-center">
                <p className="text-xs text-gray-500">
                  Demo credentials: hi@cuanbot.id / cuanbot2025
                </p>
              </div>
            )}
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              {mode === 'login' ? 'Belum punya akun?' : 'Sudah punya akun?'}{' '}
              <button
                onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
                className="text-blue-600 font-semibold hover:text-blue-700"
              >
                {mode === 'login' ? 'Daftar' : 'Masuk'}
              </button>
            </p>
          </div>

          {mode === 'register' && (
            <p className="mt-4 text-xs text-gray-500 text-center">
              Dengan mendaftar, Anda menyetujui{' '}
              <a href="#" className="text-blue-600 hover:underline">Terms of Service</a>
              {' '}dan{' '}
              <a href="#" className="text-blue-600 hover:underline">Privacy Policy</a>
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
