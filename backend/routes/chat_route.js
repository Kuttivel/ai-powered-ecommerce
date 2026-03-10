import express from "express";
import { chatWithAssistant } from "../controllers/chat_controller.js";

const router = express.Router();

router.post("/", chatWithAssistant);

export default router;