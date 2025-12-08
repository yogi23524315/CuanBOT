import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'CuanBot - Chatbot Akunting untuk UMKM Indonesia',
  description: 'Kelola keuangan UMKM dengan mudah menggunakan AI chatbot. Catat transaksi via chat, lihat laporan real-time, dan prediksi pendapatan.',
}

export default function LandingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <>{children}</>
}
