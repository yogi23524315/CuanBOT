'use client'

import { useState } from 'react'
import Navbar from '@/components/landing/Navbar'
import Hero from '@/components/landing/Hero'
import Benefits from '@/components/landing/Benefits'
import HowItWorks from '@/components/landing/HowItWorks'
import Features from '@/components/landing/Features'
import Pricing from '@/components/landing/Pricing'
import Testimonials from '@/components/landing/Testimonials'
import FAQ from '@/components/landing/FAQ'
import Footer from '@/components/landing/Footer'
import AuthModal from '@/components/landing/AuthModal'

export default function LandingPage() {
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)

  return (
    <div className="min-h-screen">
      <Navbar onOpenAuth={() => setIsAuthModalOpen(true)} />

      {/* Content */}
      <div className="pt-16">
        <Hero onOpenAuth={() => setIsAuthModalOpen(true)} />
        <div id="benefits">
          <Benefits />
        </div>
        <HowItWorks />
        <div id="features">
          <Features />
        </div>
        <div id="pricing">
          <Pricing onOpenAuth={() => setIsAuthModalOpen(true)} />
        </div>
        <Testimonials />
        <div id="faq">
          <FAQ />
        </div>
        
        {/* CTA Section */}
        <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl font-bold mb-6">
              Siap Kelola Keuangan dengan Lebih Mudah?
            </h2>
            <p className="text-xl mb-8 text-blue-100">
              Bergabung dengan ribuan UMKM Indonesia yang sudah merasakan manfaatnya
            </p>
            <button
              onClick={() => setIsAuthModalOpen(true)}
              className="px-8 py-4 bg-yellow-400 text-blue-900 font-bold rounded-lg hover:bg-yellow-300 transition-all transform hover:scale-105 shadow-lg text-lg"
            >
              🚀 Mulai Gratis 14 Hari
            </button>
            <p className="mt-4 text-sm text-blue-200">
              Tanpa kartu kredit • Cancel kapan saja • Garansi uang kembali
            </p>
          </div>
        </section>

        <Footer />
      </div>

      {/* Auth Modal */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
      />
    </div>
  )
}
