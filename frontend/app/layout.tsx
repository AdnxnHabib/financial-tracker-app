import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Financial Tracker",
  description: "A personal finance dashboard for tracking expenses.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
