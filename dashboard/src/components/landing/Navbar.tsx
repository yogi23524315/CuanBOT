'use client'

interface NavbarProps {
  onOpenAuth: () => void
}

export default function Navbar({ onOpenAuth }: NavbarProps) {
  return (
    <nav className="fixed top-0 left-0 right-0 z-40 bg-white/90 backdrop-blur-md shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-2">
            <img src="/cuanbot-logo.png" alt="CuanBot Logo" className="h-8" />
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a href="#benefits" className="text-gray-700 hover:text-blue-600 transition-colors">Benefit</a>
            <a href="#features" className="text-gray-700 hover:text-blue-600 transition-colors">Fitur</a>
            <a href="#pricing" className="text-gray-700 hover:text-blue-600 transition-colors">Harga</a>
            <a href="#faq" className="text-gray-700 hover:text-blue-600 transition-colors">FAQ</a>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={onOpenAuth}
              className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
            >
              Masuk
            </button>
            <button
              onClick={onOpenAuth}
              className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
            >
              Daftar Gratis
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
