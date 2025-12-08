export default function Benefits() {
  const benefits = [
    {
      icon: '⚡',
      title: 'Cepat & Mudah',
      description: 'Catat transaksi hanya dengan chat natural language. Tidak perlu form rumit atau training khusus.'
    },
    {
      icon: '🤖',
      title: 'AI Powered',
      description: 'Teknologi AI Gemini yang memahami bahasa Indonesia dan otomatis kategorisasi transaksi.'
    },
    {
      icon: '📊',
      title: 'Laporan Real-time',
      description: 'Dashboard cantik dengan grafik dan analisis keuangan yang update otomatis setiap saat.'
    },
    {
      icon: '🔮',
      title: 'Prediksi Akurat',
      description: 'Machine Learning Prophet untuk forecasting pendapatan 30 hari ke depan dengan akurasi tinggi.'
    },
    {
      icon: '🚨',
      title: 'Deteksi Anomali',
      description: 'Sistem cerdas mendeteksi transaksi mencurigakan dan melindungi bisnis Anda dari fraud.'
    },
    {
      icon: '📱',
      title: 'Mobile Friendly',
      description: 'Akses dari mana saja via Telegram dan dashboard responsive yang works di semua device.'
    }
  ]

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Kenapa Pilih CuanBot?
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Solusi akunting modern yang dirancang khusus untuk UMKM Indonesia
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {benefits.map((benefit, index) => (
            <div
              key={index}
              className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-2"
            >
              <div className="text-5xl mb-4">{benefit.icon}</div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">{benefit.title}</h3>
              <p className="text-gray-600">{benefit.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
