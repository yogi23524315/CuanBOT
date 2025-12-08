'use client'

interface HeroProps {
  onOpenAuth: () => void
}

export default function Hero({ onOpenAuth }: HeroProps) {
  return (
    <section className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white overflow-hidden">
      <div className="absolute inset-0 bg-grid-white/[0.05] bg-[size:20px_20px]" />
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="text-center lg:text-left">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              Kelola Keuangan UMKM Anda dengan <span className="text-yellow-300">Mudah & Cerdas</span>
            </h1>
            <p className="text-xl sm:text-2xl mb-8 text-blue-100">
              CuanBot - Chatbot Akunting berbasis AI yang membantu UMKM Indonesia mencatat transaksi hanya dengan chat!
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <button
                onClick={onOpenAuth}
                className="px-8 py-4 bg-yellow-400 text-blue-900 font-bold rounded-lg hover:bg-yellow-300 transition-all transform hover:scale-105 shadow-lg text-lg"
              >
                🚀 Mulai Gratis Sekarang
              </button>
              <button className="px-8 py-4 bg-white/10 backdrop-blur-sm border-2 border-white/30 text-white font-semibold rounded-lg hover:bg-white/20 transition-all text-lg">
                📹 Lihat Demo
              </button>
            </div>
            <p className="mt-6 text-blue-200 text-sm">
              ✨ Gratis 14 hari trial • Tanpa kartu kredit • Setup 5 menit
            </p>
          </div>
          <div className="hidden lg:block">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-yellow-400 to-pink-500 rounded-3xl blur-3xl opacity-30 animate-pulse" />
              <div className="relative bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20 shadow-2xl">
                <div className="space-y-4">
                  <div className="bg-white/20 rounded-lg p-4 animate-slide-in">
                    <p className="text-sm text-blue-100 mb-2">💬 Chat dengan bot:</p>
                    <p className="font-semibold">"Terima uang 500rb dari customer"</p>
                  </div>
                  <div className="bg-green-500/20 rounded-lg p-4 animate-slide-in" style={{ animationDelay: '0.2s' }}>
                    <p className="text-sm text-green-100 mb-2">✅ Otomatis tercatat:</p>
                    <p className="font-semibold">Pemasukan: Rp 500.000</p>
                  </div>
                  <div className="bg-blue-500/20 rounded-lg p-4 animate-slide-in" style={{ animationDelay: '0.4s' }}>
                    <p className="text-sm text-blue-100 mb-2">📊 Laporan instant:</p>
                    <p className="font-semibold">Saldo: Rp 2.500.000</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
