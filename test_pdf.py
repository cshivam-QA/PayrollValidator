from dashboard.pdf_generator import PDFGenerator

pdf = PDFGenerator()

output = pdf.generate(

    template_name="store_details_pdf.html",

    context={

        "integration":"Food Out",

        "store":"1056",

        "business_date":"2026-07-20",

        "status":"PASS"

    },

    output_filename="Test.pdf"

)

print(output)