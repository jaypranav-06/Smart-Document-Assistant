import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Smart Document Assistant - AI-Powered PDF Analysis",
  description: "Extract insights from your PDF documents with AI-powered answers and precise citations. Upload, ask questions, and get instant answers backed by source references.",
  keywords: ["PDF analysis", "document AI", "question answering", "citation extraction", "AI assistant"],
  authors: [{ name: "Smart Document Assistant Team" }],
  openGraph: {
    title: "Smart Document Assistant",
    description: "AI-powered PDF analysis with precise citations",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
