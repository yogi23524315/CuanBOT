'use client'

import { useState } from 'react'
import { ChevronDown } from 'lucide-react'

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0)

  const faqs = [
    {
      question: 'Apa itu CuanBot?',
      answer: 'CuanBot adalah chatbot akunting berbasis AI yang membantu UMKM Indonesia mengelola keuangan dengan mudah. Cukup chat via Telegram untuk mencatat transaksi, dan lihat laporan lengkap di dashboard.'
    },
    {
      question: 'Bagaimana cara kerja CuanBot?',
      answer: 'Sangat mudah! Anda hanya perlu mengirim pesan ke bot Telegram seperti "Terima uang 500rb dari customer" atau "Bayar listrik 300 ribu". AI kami akan otomatis memproses dan mencatat transaksi tersebut.'
    },
    {
      question: 'Apakah data saya aman?',
      answer: 'Sangat aman! Kami menggunakan enkripsi tingkat bank, database terproteksi, dan tidak pernah membagikan data Anda ke pihak ketiga. Semua data disimpan di server Indonesia.'
    },
    {
      question: 'Berapa lama trial gratis?',
      answer: 'Kami memberikan trial gratis selama 14 hari penuh dengan akses ke semua fitur. Tidak perlu kartu kredit untuk mendaftar. Jika tidak cocok, bisa cancel kapan saja.'
    },
    {
      question: 'Apakah bisa untuk multiple user?',
      answer: 'Ya! Paket Personal untuk 1 user, dan paket UMKM untuk 5 user. Semua user bisa akses bot dan dashboard dengan data yang tersinkronisasi real-time.'
    },
    {
      question: 'Bagaimana cara pembayaran?',
      answer: 'Kami menerima pembayaran via transfer bank, e-wallet (GoPay, OVO, Dana), dan kartu kredit. Pembayaran bulanan otomatis dan bisa cancel kapan saja.'
    },
    {
      question: 'Apakah ada training atau panduan?',
      answer: 'Tentu! Kami menyediakan video tutorial, dokumentasi lengkap, dan untuk paket UMKM ada onboarding session 1-on-1 dengan tim kami.'
    },
    {
      question: 'Bisa export laporan untuk pajak?',
      answer: 'Bisa! Anda bisa export laporan dalam format PDF dan Excel yang sudah sesuai standar akunting Indonesia, siap untuk keperluan pajak dan audit.'
    }
  ]

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Frequently Asked Questions
          </h2>
          <p className="text-xl text-gray-600">
            Pertanyaan yang sering ditanyakan
          </p>
        </div>
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span className="font-semibold text-gray-900 pr-4">{faq.question}</span>
                <ChevronDown
                  className={`w-5 h-5 text-gray-500 flex-shrink-0 transition-transform ${
                    openIndex === index ? 'transform rotate-180' : ''
                  }`}
                />
              </button>
              {openIndex === index && (
                <div className="px-6 pb-4 text-gray-600">
                  {faq.answer}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
