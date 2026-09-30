from fastapi import FastAPI,APIRouter,Request,Form,HTTPException
app = FastAPI()
@app.get("/")
async def home():
    return{"message":"Comic-Craft AI is live"}
router = APIRouter()
# Comic Generation Route
@router.post("/generate")
async def generate_comic(
    request: Request,
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    style: str = Form(...)
):
    try:
        # Combine user inputs into a single full prompt
        full_prompt = f"""
        Story Prompt: {prompt}
        Main Character: {character_name}
        Setting: {setting}
        Tone: {tone}
        Style: {style}
        """

        # Step 1: Generate panel outline
        outline = generate_outline(full_prompt)

        if not isinstance(outline, list) or len(outline) != 5:
            raise Exception("Failed to outline story into 5 panels")

        # Step 2: Generate story
        full_story = generate_story(outline)

        # Step 3: Generate images
        images = [generate_image(panel["image_prompt"]) for panel in outline]

        # Step 4: Build layout
        layout = build_comic_layout(images, full_story, outline)

        # Step 5: Export to PDF
        pdf_path = save_pdf(layout)
        set_pdf_path(pdf_path)  # Sets global PDF path for export

        return templates.TemplateResponse("comic_preview.html", {
            "request": request,
            "layout": layout,
            "pdf_path": pdf_path
        })

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Export Success Route
@router.get("/export-success")
async def export_success(request: Request, pdf_path: str):
    return templates.TemplateResponse("export_success.html", {
        "request": request,
        "pdf_path": pdf_path
    })


# Image Generation Route
@router.get("/test-image")
async def test_image(prompt: str = "A futuristic city at sunset, sci-fi, cinematic, detailed"):
    try:
        image_path = generate_image(prompt)
        return {"message": "Image generated successfully", "path": image_path}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

app.include_router(router)
