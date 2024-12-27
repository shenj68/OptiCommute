import { NextResponse } from "next/server";
import path from "path";
import { writeFile } from "fs/promises";

// POST handler for file upload
export const POST = async (req) => {
    const formData = await req.formData();

    const file = formData.get("file");

    if (!file) {
        return NextResponse.json({ error: "No files received.", status: 400 });
    }

    // convert file data to a buffer
    const buffer = Buffer.from(await file.arrayBuffer());

    const fileName = file.name.replaceAll(" ", "_");
    console.log(fileName);

    // create the path to the videos directory
    const videosDir = path.join(process.cwd(), "videos");
    const filePath = path.join(videosDir, fileName);

    try {
        await writeFile(filePath, buffer);

        return NextResponse.json({
            Message: "File uploaded successfully.",
            status: 200,
        });
    } catch (error) {
        console.log("Error occured ", error);
        return NextResponse.json({
            Message: "Error uploading file.",
            status: 500,
        });
    }
};
