import { Config } from "@remotion/cli/config";
// 像素画：帧用 PNG，不让 JPEG 在像素边上糊出杂色
Config.setVideoImageFormat("png");
