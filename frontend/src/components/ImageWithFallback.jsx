import { useState } from "react";

export function ImageWithFallback({ src, alt, className = "", fallbackClassName = "", fallbackText = "No image" }) {
    const [has_error, set_has_error] = useState(false);

    if (!src || has_error) {
        return <div className={fallbackClassName || className}>{fallbackText}</div>;
    }

    return (
        <img
            className={className}
            src={src}
            alt={alt}
            loading="lazy"
            onError={() => set_has_error(true)}
        />
    );
}