import { Route, Routes } from "react-router-dom";
import { useState } from "react";
import { Navbar } from "./components/Navbar.jsx";
import { ChatAssistant } from "./components/ChatAssistant.jsx";
import { HomePage } from "./pages/HomePage.jsx";
import { ProductPage } from "./pages/ProductPage.jsx";

function App() {
    const [chat_open, set_chat_open] = useState(false);

    return (
        <div className="app_shell">
            <Navbar />
            <main className="page_shell">
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/products/:productId" element={<ProductPage />} />
                </Routes>
            </main>
            <ChatAssistant
                isOpen={chat_open}
                onOpen={() => set_chat_open(true)}
                onClose={() => set_chat_open(false)}
            />
        </div>
    );
}

export default App;