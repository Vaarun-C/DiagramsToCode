import { Open_Sans } from "next/font/google";
import "./globals.css";

const inter = Open_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <head>
        <title>Diagrams To Code</title>
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
