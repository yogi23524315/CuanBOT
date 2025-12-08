export default function Testimonials() {
  const testimonials = [
    {
      name: 'Budi Santoso',
      role: 'Pemilik Warung Makan',
      location: 'Jakarta',
      avatar: '👨‍🍳',
      rating: 5,
      text: 'CuanBot sangat membantu! Dulu saya bingung catat keuangan, sekarang tinggal chat aja. Laporan langsung jadi dan bisa lihat untung rugi dengan mudah.'
    },
    {
      name: 'Siti Nurhaliza',
      role: 'Online Shop Owner',
      location: 'Bandung',
      avatar: '👩‍💼',
      rating: 5,
      text: 'Fitur forecasting-nya keren banget! Bisa prediksi pendapatan bulan depan jadi bisa planning stok dengan lebih baik. Recommended!'
    },
    {
      name: 'Ahmad Rizki',
      role: 'Freelance Designer',
      location: 'Surabaya',
      avatar: '👨‍💻',
      rating: 5,
      text: 'Sebagai freelancer, CuanBot bikin hidup lebih mudah. Catat invoice, track pembayaran client, semua otomatis. Dashboard-nya juga keren!'
    },
    {
      name: 'Dewi Lestari',
      role: 'Pemilik Toko Baju',
      location: 'Yogyakarta',
      avatar: '👩‍🦱',
      rating: 5,
      text: 'Harga terjangkau dengan fitur lengkap. Deteksi anomali-nya membantu saya ketahuan ada transaksi yang tidak wajar. Worth it banget!'
    }
  ]

  return (
    <section className="py-20 bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">
            Apa Kata Mereka?
          </h2>
          <p className="text-xl text-blue-100">
            Ribuan UMKM Indonesia sudah merasakan manfaatnya
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
              <div className="flex items-center gap-3 mb-4">
                <div className="text-4xl">{testimonial.avatar}</div>
                <div>
                  <h4 className="font-bold">{testimonial.name}</h4>
                  <p className="text-sm text-blue-200">{testimonial.role}</p>
                  <p className="text-xs text-blue-300">{testimonial.location}</p>
                </div>
              </div>
              <div className="flex gap-1 mb-3">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <span key={i} className="text-yellow-400">⭐</span>
                ))}
              </div>
              <p className="text-blue-50 italic">"{testimonial.text}"</p>
            </div>
          ))}
        </div>
        <div className="text-center mt-12">
          <div className="inline-flex items-center gap-8 bg-white/10 backdrop-blur-lg rounded-full px-8 py-4 border border-white/20">
            <div>
              <div className="text-3xl font-bold">1000+</div>
              <div className="text-sm text-blue-200">UMKM Aktif</div>
            </div>
            <div className="w-px h-12 bg-white/20" />
            <div>
              <div className="text-3xl font-bold">4.9/5</div>
              <div className="text-sm text-blue-200">Rating</div>
            </div>
            <div className="w-px h-12 bg-white/20" />
            <div>
              <div className="text-3xl font-bold">50K+</div>
              <div className="text-sm text-blue-200">Transaksi/Hari</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
