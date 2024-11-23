'use client';

import { useRouter } from 'next/navigation';

export default function LandingPage() {
  const router = useRouter();

  // Function to navigate to the login page
  const goToLogin = () => {
    router.push('/auth/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-indigo-600 text-white flex flex-col justify-center items-center">
      {/* Hero Section */}
      <section className="text-center px-4 py-12 max-w-2xl mx-auto">
        <h1 className="text-5xl font-bold mb-4">Meet Your AI Assistant</h1>
        <p className="text-lg mb-6">Your personal assistant for summarizing and taking notes—just speak, and let the AI do the rest.</p>
        <button
          onClick={goToLogin}
          className="px-6 py-3 bg-indigo-700 rounded-lg text-white text-xl font-semibold hover:bg-indigo-800 transition duration-300"
        >
          Get Started
        </button>
      </section>

      {/* Features Section */}
      <section className="w-full bg-gray-800 py-16 mt-16">
        <div className="text-center text-white px-6 max-w-4xl mx-auto">
          <h2 className="text-3xl font-semibold mb-6">What I Can Do For You</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gray-900 p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-semibold mb-3">Summarize Meetings</h3>
              <p>Let me listen to your meetings and provide concise summaries so you can stay informed without the hassle.</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-semibold mb-3">Take Notes</h3>
              <p>Need to note something down? Just speak, and Ill take care of your notes for you.</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-lg shadow-lg">
              <h3 className="text-xl font-semibold mb-3">Voice Commands</h3>
              <p>Control everything with your voice—summarize, take notes, and more, hands-free!</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="bg-gray-900 w-full text-center py-6 mt-16">
        <p>&copy; 2024 Your AI Assistant. All rights reserved.</p>
      </footer>
    </div>
  );
}
