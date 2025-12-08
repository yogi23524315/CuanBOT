export default function Features() {
  const features = [
    {
      category: 'Telegram Bot',
      items: [
        'Natural Language Processing',
        'Auto Kategorisasi',
        'Multi-tipe Transaksi',
        'Ringkasan Otomatis',
        'Q&A Akunting'
      ]
    },
    {
      category: 'Dashboard Web',
      items: [
        'Real-time Monitoring',
        'Beautiful Charts',
        'Responsive Design',
        'Export PDF/Excel',
        'Filter & Search'
      ]
    },
    {
      category: 'AI & Machine Learning',
      items: [
        'Forecasting Prophet',
        'Anomaly Detection',
        'Smart Insights',
        'Trend Analysis',
        'Predictive Analytics'
      ]
    },
    {
      category: 'Reporting',
      items: [
        'Laporan Keuangan',
        'Laba Rugi',
        'Arus Kas',
        'Neraca',
        'Custom Reports'
      ]
    }
  ]

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Fitur Lengkap CuanBot
          </h2>
          <p className="text-xl text-gray-600">
            Semua yang Anda butuhkan untuk kelola keuangan UMKM
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-100">
              <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span className="text-2xl">
                  {index === 0 ? '💬' : index === 1 ? '📊' : index === 2 ? '🤖' : '📄'}
                </span>
                {feature.category}
              </h3>
              <ul className="space-y-2">
                {feature.items.map((item, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-gray-700">
                    <span className="text-green-500">✓</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
