export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <span className="text-xl font-bold text-white">CuanBOT</span>
            </div>
            <p className="text-sm mb-4">
              Chatbot Akunting berbasis AI untuk UMKM Indonesia
            </p>
            <div className="flex gap-4">
              <a href="#" className="hover:text-white transition-colors">📘 Facebook</a>
              <a href="#" className="hover:text-white transition-colors">📷 Instagram</a>
              <a href="#" className="hover:text-white transition-colors">🐦 Twitter</a>
            </div>
          </div>
          <div>
            <h4 className="font-bold text-white mb-4">Produk</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white transition-colors">Fitur</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Harga</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Demo</a></li>
              <li><a href="#" className="hover:text-white transition-colors">API</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-white mb-4">Perusahaan</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white transition-colors">Tentang Kami</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Karir</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Kontak</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold text-white mb-4">Bantuan</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="#" className="hover:text-white transition-colors">Dokumentasi</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Tutorial</a></li>
              <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
              <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm">
            © 2024 CuanBot. All rights reserved. Made with ❤️ for Indonesian UMKM
          </p>
          <div className="flex gap-6 text-sm">
            <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
            <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
            <a href="#" className="hover:text-white transition-colors">Cookie Policy</a>
          </div>
        </div>
      </div>
    </footer>
  )
}
