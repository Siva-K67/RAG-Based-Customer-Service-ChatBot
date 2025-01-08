import express from "express";
import { isAuth } from "../middlewares/isAuth.js";
import {
  addConversation,
  createChat,
  deleteChat,
  getAllChats,
  getConversation,
} from "../controllers/chatControllers.js";

const router = express.Router();

router.post("/new", isAuth, createChat);
router.get("/all", isAuth, getAllChats);
router.post("/:id", isAuth, addConversation);
router.get("/:id", isAuth, getConversation);
router.delete("/:id", isAuth, deleteChat);

export default router;
// 2024-10-18 18:30:54 - fake change 1
// 2024-10-20 13:50:15 - fake change 1
// 2024-10-30 13:27:11 - fake change 2
// 2024-11-05 13:16:50 - fake change 3
// 2024-11-06 14:52:5 - fake change 4
// 2024-11-27 9:2:16 - fake change 2
// 2024-12-07 17:59:7 - fake change 1
// 2024-12-15 11:3:10 - fake change 3
// 2025-01-01 12:2:35 - fake change 3
// 2024-12-29 10:55:10 - fake change 4
// 2025-01-08 12:16:2 - fake change 1
