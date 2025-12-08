export default function HowItWorks() {
  const steps = [
    {
      number: '1',
      title: 'Daftar & Setup',
      description: 'Buat akun dan hubungkan Telegram bot dalam 5 menit. Gratis trial 14 hari!',
      icon: '📝'
    },
    {
      number: '2',
      title: 'Chat dengan Bot',
      description: 'Kirim pesan seperti "Terima uang 500rb" atau "Bayar listrik 300 ribu" via Telegram.',
      icon: '💬'
    },
    {
      number: '3',
      title: 'Otomatis Tercatat',
      description: 'AI memproses dan mencatat transaksi Anda secara otomatis dengan kategori yang tepat.',
      icon: '✨'
    },
    {
      number: '4',
      title: 'Lihat Laporan',
      description: 'Akses dashboard untuk melihat grafik, prediksi, dan export laporan PDF profesional.',
      icon: '📊'
    }
  ]

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Cara Penggunaan
          </h2>
          <p className="text-xl text-gray-600">
            Mulai kelola keuangan dalam 4 langkah mudah
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              {index < steps.length - 1 && (
                <div className="hidden lg:block absolute top-16 left-full w-full h-0.5 bg-gradient-to-r from-blue-500 to-transparent -translate-x-1/2" />
              )}
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 text-white rounded-full text-2xl font-bold mb-4 shadow-lg">
                  {step.number}
                </div>
                <div className="text-4xl mb-4">{step.icon}</div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{step.title}</h3>
                <p className="text-gray-600">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
