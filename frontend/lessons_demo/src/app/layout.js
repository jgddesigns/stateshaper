import "./globals.css";



export const metadata = {
  title: "Stateshaper Lesson Plan Demo",
  description: "Content Generation using Perpetual Determinism",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className=""
      >
        {children}
      </body>
    </html>
  );
}
