'use client'

interface PricingProps {
  onOpenAuth: () => void
}

export default function Pricing({ onOpenAuth }: PricingProps) {
  const plans = [
    {
      name: 'Personal',
      description: 'Untuk freelancer & usaha kecil',
      originalPrice: '50.000',
      price: '25.000',
      period: '/bulan',
      features: [
        '✅ 1 User Telegram',
        '✅ Unlimited Transaksi',
        '✅ Dashboard Real-time',
        '✅ Laporan PDF',
        '✅ AI Chatbot',
        '✅ Forecasting 30 hari',
        '✅ Deteksi Anomali',
        '✅ Support Email'
      ],
      popular: false,
      color: 'blue'
    },
    {
      name: 'UMKM',
      description: 'Untuk bisnis yang berkembang',
      originalPrice: '100.000',
      price: '50.000',
      period: '/bulan',
      features: [
        '✅ 5 User Telegram',
        '✅ Unlimited Transaksi',
        '✅ Dashboard Real-time',
        '✅ Laporan PDF Unlimited',
        '✅ AI Chatbot Advanced',
        '✅ Forecasting 90 hari',
        '✅ Deteksi Anomali Premium',
        '✅ Multi-kategori Custom',
        '✅ Export Excel',
        '✅ Priority Support',
        '✅ Training & Onboarding'
      ],
      popular: true,
      color: 'indigo'
    }
  ]

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Paket Berlangganan
          </h2>
          <p className="text-xl text-gray-600 mb-4">
            Pilih paket yang sesuai dengan kebutuhan bisnis Anda
          </p>
          <div className="inline-flex items-center gap-2 bg-green-100 text-green-800 px-4 py-2 rounded-full font-semibold">
            🎉 Promo Spesial - Diskon hingga 50%!
          </div>
        </div>
        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`relative bg-white rounded-2xl shadow-xl overflow-hidden transform transition-all hover:scale-105 ${
                plan.popular ? 'ring-4 ring-indigo-500' : ''
              }`}
            >
              {plan.popular && (
                <div className="absolute top-0 right-0 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-2 rounded-bl-2xl font-bold">
                  🔥 TERPOPULER
                </div>
              )}
              <div className="p-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <p className="text-gray-600 mb-6">{plan.description}</p>
                <div className="mb-6">
                  <div className="flex items-baseline gap-2 mb-2">
                    <span className="text-gray-400 line-through text-xl">Rp {plan.originalPrice}</span>
                    <span className="bg-red-100 text-red-600 px-2 py-1 rounded text-sm font-bold">-50%</span>
                  </div>
                  <div className="flex items-baseline">
                    <span className="text-5xl font-bold text-gray-900">Rp {plan.price}</span>
                    <span className="text-gray-600 ml-2">{plan.period}</span>
                  </div>
                </div>
                <button
                  onClick={onOpenAuth}
                  className={`w-full py-4 rounded-lg font-bold text-lg transition-all mb-6 ${
                    plan.popular
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white hover:from-indigo-700 hover:to-purple-700 shadow-lg'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  Mulai Gratis 14 Hari
                </button>
                <ul className="space-y-3">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-gray-700">
                      <span className="text-green-500 flex-shrink-0">{feature.split(' ')[0]}</span>
                      <span>{feature.substring(feature.indexOf(' ') + 1)}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
        <p className="text-center text-gray-600 mt-8">
          💳 Semua paket include gratis trial 14 hari • Bisa cancel kapan saja • Garansi uang kembali 30 hari
        </p>
      </div>
    </section>
  )
}
