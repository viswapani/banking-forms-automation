from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FORMS = [
    "Account Opening",
    "Cheque Book Request",
    "ATM Card Block/Replacement",
    "Address Change Request",
    "RTGS/NEFT Transfer",
    "KYC Update",
    "Locker Access/Surrender",
]

# Simple fixed test data to render on each form
TEST_DATA = {
    "Customer Name": "John Doe",
    "Account Number": "1234567890",
    "Email": "john.doe@example.com",
    "Mobile": "+91-9876543210",
    "Branch Code": "BR001",
    "Address": "123 Main Street, Cityville",
}


def slugify(name: str) -> str:
    return (
        name.lower()
        .replace("/", "_")
        .replace(" ", "_")
        .replace("__", "_")
        .replace("-", "_")
    )


def create_form_image(form_name: str, output_dir: Path) -> Path:
    width, height = 1000, 1400
    background_color = "white"
    text_color = "black"

    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Try default font; Pillow will pick something
    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_label = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        # Fallback if arial.ttf isn't available
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()

    margin = 80
    current_y = 80

    # Draw form title
    draw.text((margin, current_y), f"Bank XYZ - {form_name} Form", fill=text_color, font=font_title)
    current_y += 80

    # Draw a line under the title
    draw.line((margin, current_y, width - margin, current_y), fill="black", width=2)
    current_y += 40

    # Draw static test fields
    for label, value in TEST_DATA.items():
        line = f"{label}: {value}"
        draw.text((margin, current_y), line, fill=text_color, font=font_label)
        current_y += 50

    # Add a few form-specific hints/fields
    current_y += 40
    if form_name == "Cheque Book Request":
        extra = [
            "Number of cheque leaves requested: 25",
            "Delivery Option: Collect at Branch",
        ]
    elif form_name == "ATM Card Block/Replacement":
        extra = [
            "ATM Card Number: 5555 6666 7777 8888",
            "Reason: Lost card",
            "Request: Block existing card and issue replacement",
        ]
    elif form_name == "Address Change Request":
        extra = [
            "Old Address: 45 Old Street, Old City",
            "New Address: 789 New Avenue, New City",
        ]
    elif form_name == "RTGS/NEFT Transfer":
        extra = [
            "Beneficiary Name: Jane Smith",
            "Beneficiary Account: 9876543210",
            "IFSC Code: XYZB0000123",
            "Amount: 25,000 INR",
            "Transfer Type: NEFT",
        ]
    elif form_name == "KYC Update":
        extra = [
            "Document Type: PAN Card",
            "Document Number: ABCDE1234F",
            "KYC Status: Update existing details",
        ]
    elif form_name == "Locker Access/Surrender":
        extra = [
            "Locker Number: L-123",
            "Branch Locker Section: A",
            "Request Type: Surrender",
        ]
    else:  # Account Opening or others
        extra = [
            "Account Type: Savings",
            "Initial Deposit: 10,000 INR",
        ]

    for line in extra:
        draw.text((margin, current_y), line, fill=text_color, font=font_label)
        current_y += 50

    # Save image
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(form_name)}.png"
    output_path = output_dir / filename
    img.save(output_path, format="PNG")
    return output_path


def main():
    base_dir = Path(__file__).resolve().parents[2]  # go up to project root
    output_dir = base_dir / "test_forms"

    print(f"Generating test forms in: {output_dir}")
    for form_name in FORMS:
        path = create_form_image(form_name, output_dir)
        print(f"Created: {path}")


if __name__ == "__main__":
    main()