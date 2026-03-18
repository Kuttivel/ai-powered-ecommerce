import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { sendChatMessage } from "../lib/api.js";
import { ImageWithFallback } from "./ImageWithFallback.jsx";

export function ChatAssistant({ isOpen, onOpen, onClose }) {
    const [message, set_message] = useState("");
    const [submitting, set_submitting] = useState(false);
    const [session_id, set_session_id] = useState("");
    const [conversation, set_conversation] = useState([]);
    const [product_results, set_product_results] = useState([]);
    const messages_ref = useRef(null);

    useEffect(() => {
        if (!messages_ref.current) {
            return;
        }

        messages_ref.current.scrollTop = messages_ref.current.scrollHeight;
    }, [conversation, product_results, isOpen]);

    async function handle_submit(event) {
        event.preventDefault();

        if (!message.trim() || submitting) {
            return;
        }

        const user_message = message.trim();
        set_message("");
        set_submitting(true);
        set_conversation((current) => [...current, { role: "user", text: user_message }]);

        try {
            const data = await sendChatMessage({
                message: user_message,
                session_id,
            });

            set_session_id(data.session_id || session_id);
            set_product_results(data.products || []);
            set_conversation((current) => [...current, { role: "assistant", text: data.reply || "No response received." }]);
        }
        catch (error) {
            set_product_results([]);
            set_conversation((current) => [...current, { role: "assistant", text: error.message || "Unable to get assistant response." }]);
        }
        finally {
            set_submitting(false);
        }
    }

    function handle_key_down(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handle_submit(event);
        }
    }

    return (
        <>
            {!isOpen ? (
                <button className="chat_fab" type="button" onClick={onOpen}>
                    Assistant
                </button>
            ) : null}

            <div className={isOpen ? "drawer_backdrop visible" : "drawer_backdrop"} onClick={onClose} />

            <aside className={isOpen ? "chat_drawer open" : "chat_drawer"}>
                <div className="chat_drawer_header">
                    <div>
                        <h3>Conversational product search</h3>
                        <p>Ask for products, brands, budget options, or say hello.</p>
                    </div>

                    <button className="drawer_close_button" type="button" onClick={onClose}>
                        Close
                    </button>
                </div>

                <div className="chat_body" ref={messages_ref}>
                    {!conversation.length ? (
                        <div className="chat_hint_box">
                            <p>Try asking:</p>
                            <ul>
                                <li>hello</li>
                                <li>show me budget watches</li>
                                <li>find shoes under £20</li>
                                <li>cheaper options</li>
                            </ul>
                        </div>
                    ) : null}

                    {conversation.map((item, index) => (
                        <div
                            key={`${item.role}-${index}`}
                            className={item.role === "user" ? "chat_bubble user" : "chat_bubble assistant"}
                        >
                            {item.text}
                        </div>
                    ))}

                    {product_results.length ? (
                        <div className="chat_products">
                            <h4>Suggested products</h4>
                            <div className="chat_product_list">
                                {product_results.map((product) => (
                                    <Link
                                        className="chat_product_item"
                                        key={product.id}
                                        to={`/products/${product.id}`}
                                        onClick={onClose}
                                    >
                                        <ImageWithFallback
                                            src={product.imageUrl}
                                            alt={product.name}
                                            className="chat_product_image"
                                            fallbackClassName="chat_product_placeholder"
                                            fallbackText="No image"
                                        />

                                        <div className="chat_product_text">
                                            <strong>{product.name}</strong>
                                            <p>{product.priceDisplay || "Price unavailable"}</p>
                                        </div>
                                    </Link>
                                ))}
                            </div>
                        </div>
                    ) : null}
                </div>

                <form className="chat_form" onSubmit={handle_submit}>
                    <textarea
                        rows="3"
                        value={message}
                        onChange={(event) => set_message(event.target.value)}
                        onKeyDown={handle_key_down}
                        placeholder="Type your message or product search request"
                    />

                    <button className="primary_button full_width_button" type="submit" disabled={submitting}>
                        {submitting ? "Sending..." : "Send"}
                    </button>
                </form>
            </aside>
        </>
    );
}