'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { LayoutDashboard, FileText, Menu, X, LogOut } from 'lucide-react'

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()
  const router = useRouter()
  const [userEmail, setUserEmail] = useState('')

  useEffect(() => {
    const email = localStorage.getItem('userEmail')
    if (email) setUserEmail(email)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('userEmail')
    router.push('/landing')
  }

  const menuItems = [
    {
      name: 'Dashboard',
      href: '/',
      icon: LayoutDashboard,
    },
    {
      name: 'Reporting',
      href: '/reports',
      icon: FileText,
    },
  ]

  const isActive = (href: string) => {
    if (href === '/') {
      return pathname === '/'
    }
    return pathname.startsWith(href)
  }

  return (
    <>
      {/* Mobile Menu Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-white shadow-lg hover:bg-gray-50"
      >
        {isOpen ? (
          <X className="w-6 h-6 text-gray-700" />
        ) : (
          <Menu className="w-6 h-6 text-gray-700" />
        )}
      </button>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 z-40 h-screen transition-transform duration-300 ease-in-out
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 lg:static
          w-64 bg-white border-r border-gray-200 shadow-lg lg:shadow-none
        `}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center gap-3 px-6 py-5 border-b border-gray-200">
            <img src="/cuanbot-logo.png" alt="CuanBot Logo" className="h-8" />
            <div className="flex flex-col">
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
            {menuItems.map((item) => {
              const Icon = item.icon
              const active = isActive(item.href)
              
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-lg transition-colors
                    ${active
                      ? 'bg-blue-50 text-blue-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-100'
                    }
                  `}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-gray-200">
            {userEmail && (
              <div className="mb-3 pb-3 border-b border-gray-200">
                <p className="text-xs text-gray-500 mb-1">Logged in as:</p>
                <p className="text-sm font-medium text-gray-700 truncate">{userEmail}</p>
              </div>
            )}
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
            <div className="text-xs text-gray-500 mt-3">
              <p className="font-medium text-gray-700 mb-1">CuanBot v1.2</p>
              <p>Akunting Chatbot untuk UMKM</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}
