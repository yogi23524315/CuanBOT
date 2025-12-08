'use client'

import { usePathname, useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import Sidebar from './Sidebar'

export default function ConditionalLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isChecking, setIsChecking] = useState(true)
  
  useEffect(() => {
    // Check authentication status
    const authStatus = localStorage.getItem('isAuthenticated')
    setIsAuthenticated(authStatus === 'true')
    setIsChecking(false)
    
    // Redirect to landing if not authenticated and not on landing page
    if (authStatus !== 'true' && !pathname?.startsWith('/landing')) {
      router.push('/landing')
    }
  }, [pathname, router])
  
  // Landing page tidak menggunakan sidebar
  if (pathname?.startsWith('/landing')) {
    return <>{children}</>
  }

  // Show loading while checking auth
  if (isChecking) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // Redirect if not authenticated
  if (!isAuthenticated) {
    return null
  }

  // Dashboard pages menggunakan sidebar
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto bg-gray-50">
        {children}
      </main>
    </div>
  )
}
