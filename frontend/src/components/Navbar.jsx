import { Link, useLocation } from "react-router-dom";

export function Navbar() {
    const location = useLocation();

    return (
        <header className="navbar">
            <div className="navbar_inner">
                <Link className="brand_link" to="/">
                    <span className="brand_title">AI-Powered E-Commerce</span>
                    <span className="brand_subtitle">Fake review detection and conversational search</span>
                </Link>

                <nav className="navbar_links">
                    <Link className={location.pathname === "/" ? "nav_link active" : "nav_link"} to="/">
                        Home
                    </Link>
                </nav>
            </div>
        </header>
    );
}