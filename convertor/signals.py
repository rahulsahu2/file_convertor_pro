from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import convert_pdf_to_csv
from .models import ReceiptFile
import tabula
import tempfile
import os
import re

def check_file_type(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        return "PDF"
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return "IMAGE"
    else:
        return "UNKNOWN"

def extract_image_data(text):
    data = {}

    data['Plant'] = re.search(r'Plant\s*:\s*(\S+)', text).group(1) if re.search(r'Plant\s*:\s*(\S+)', text) else ''
    data['Order Type'] = re.search(r'Order Type\s*:\s*(\S+)', text).group(1) if re.search(r'Order Type\s*:\s*(\S+)', text) else ''
    data['Price grp'] = re.search(r'Price grp\s*:\s*(\S+)', text).group(1) if re.search(r'Price grp\s*:\s*(\S+)', text) else ''
    data['Customer'] = re.search(r'Customer\s*:\s*(\S+)', text).group(1) if re.search(r'Customer\s*:\s*(\S+)', text) else ''
    data['Customer Name'] = re.search(r'Customer Name\s*:\s*(.*?)\s*\n', text).group(1) if re.search(r'Customer Name\s*:\s*(.*?)\s*\n', text) else ''
    data['City/Destination'] = re.search(r'City/Destination\s*:\s*(.*?)\s*\n', text).group(1) if re.search(r'City/Destination\s*:\s*(.*?)\s*\n', text) else ''
    data['Invoice No.'] = re.search(r'Invoice No\.\s*:\s*(\S+)', text).group(1) if re.search(r'Invoice No\.\s*:\s*(\S+)', text) else ''
    data['Inv. Date'] = re.search(r'Inv\. Date\s*:\s*(\d+\.\d+\.\d+)', text).group(1) if re.search(r'Inv\. Date\s*:\s*(\d+\.\d+\.\d+)', text) else ''

    # Add more key-value pairs based on your header
    data['Product Code'] = re.search(r'Product Code\s*:\s*(\S+)', text).group(1) if re.search(r'Product Code\s*:\s*(\S+)', text) else ''
    data['Product Name'] = re.search(r'Product Name\s*:\s*(.*?)\s*\n', text).group(1) if re.search(r'Product Name\s*:\s*(.*?)\s*\n', text) else ''
    data['Batch No.'] = re.search(r'Batch No\.\s*:\s*(\S+)', text).group(1) if re.search(r'Batch No\.\s*:\s*(\S+)', text) else ''
    data['MRP'] = re.search(r'MRP\s*:\s*(\S+)', text).group(1) if re.search(r'MRP\s*:\s*(\S+)', text) else ''
    data['Billing Rate'] = re.search(r'Billing Rate\s*:\s*(\S+)', text).group(1) if re.search(r'Billing Rate\s*:\s*(\S+)', text) else ''
    data['Billing Quantity'] = re.search(r'Billing Quantity\s*:\s*(\S+)', text).group(1) if re.search(r'Billing Quantity\s*:\s*(\S+)', text) else ''
    data['Taxable Amt.'] = re.search(r'Taxable Amt\.\s*:\s*(\S+)', text).group(1) if re.search(r'Taxable Amt\.\s*:\s*(\S+)', text) else ''
    data['Invoice Amt'] = re.search(r'Invoice Amt\s*:\s*(\S+)', text).group(1) if re.search(r'Invoice Amt\s*:\s*(\S+)', text) else ''
    return data


def generate_csv(processed_data, fieldnames):
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='', encoding='utf-8')
    writer = csv.DictWriter(temp_file, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the rows
    for row in processed_data:
        writer.writerow(row)

    # The temporary file is not closed so that the caller can continue using it
    return temp_file


@receiver(post_save, sender=ReceiptFile)
def convert_pdf_to_csv(sender, instance, **kwargs):
    file_type = check_file_type(instance.file.path)
    
    if file_type == "PDF":
        import tempfile
        import re, csv
        print(instance, instance)
        tabula.convert_into(instance.file, instance.file.name, output_format="csv", pages=1)
        data = open(instance.file.name, 'r').read()
        
        def parse_row(row):
            print(row, 'row\n')
            # Constructing result
            result = {
                "Plant": 1309,
                "Order Type": "ZDPS",
                "Price grp": "",
                "Customer": "",
                "Customer Name": "",
                "City/Destination":"",
                "Invoice No":"",
                "Invoice Date":"",
                "Product Name": product_name.group() if product_name else None,
                "HSN/SAC Code": code.group() if code else None,
                "CAT": cat.group(2) if cat else None,
                "BATCH": batch.group(1) if batch else None,
                "MFG.NAME": mfg_name.group() if mfg_name else None,
                "MFG.DT": dates[0] if dates else None,
                "EXP.DT": dates[1] if dates else None,
                "GST Rate (%)": numerics[0] if numerics else None,
                "BILLED QTY": numerics[1] if numerics else None,
                "FREE QTY": numerics[2] if numerics else None,
                "MRP": numerics[3] if numerics else None,
                "Billing Rate": numerics[4] if numerics else None,
                "Taxable Amt": numerics[5] if numerics else None,
                "DISC%": numerics[6] if numerics else None,
                "Invoice Amount": numerics[7] if numerics else None,
                "Plant Name": "",
                "Dist. channel" :"",
                "Customer State": "",
                "Customer p0 Number": "Nil",
                "PO date": "",
                "System Order No.": "",
                "Order Date": "",
                "Product type": "ZFGS",
                "Local Sales Tax NO.": "",
                "Central Sales Tax NO.":"",
                "Material Group 3": "",
                "Division":"",
                "Mfg. Plant": "",	
                "Mfg. Date": "",	
                "Exp. Date": "",	
                "Free Quantity": "",	
                "Disc.": "",	
                "Cash Disc.": "",	
                "Tax Type": "",	
                "Tax %": "",	
                "Tax Amt.": "",	
                "Add. Tax": "",	
                "Surcharge": "",	
                "Total Tax": "",	
                "LBT	Ref.": "", "Invoice No.(Returns)": "",	
                "Ref. Inv. Dt.": "",	
                "Exc. Inv. No.": "",	
                "Exc. Inv. Dt.": "",	
                "Exc. Duty %": "",	
                "Exc. Inv. Amt": "",	
                "Product Status": "",	
                "Reason For Return": "",	
                "Reason For Rejection": "",	
                "Str. Loc.": "",	
                "Sales District": "",	
                "Sales Group": "",	
                "Customer Group": "",	
                "Emp. Code": "",	
                "Employee Name": "",	
                "C Form No.": "",	
                "HSN Code": "",	
                "Business Place": "",	
                "JOCG": "",	
                "JOSG": "",	
                "JOIG": "",	
                "JOUG": "",	
                "PTR": "",	
                "PTS": "",	
                "Disc. %": "",	
                "Prod. Category": "",	
                "Prod. Category Description": "",	
                "GSTIN No. of Customer": "",	
                "GST Inv. No.": "",   
            }
            return result
        # Extracting the product data section
        product_data_section = re.search(r'PRODUCT NAME,[^*]*', data, re.DOTALL)
        if product_data_section:
            product_lines = product_data_section.group().split('\n')[1:]  # Skip the header line

        # Process each product line and store in a list
        processed_data = [parse_row(line) for line in product_lines if parse_row(line)]
        csv_file_name = 'processed_data1.csv'

        # Define the field names (columns) based on the keys of the first dictionary in the list
        fieldnames = processed_data[0].keys() if processed_data else []
        # Writing to CSV
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='', encoding='utf-8') as temp_file:
            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write the rows
            for row in processed_data:
                writer.writerow(row)
        print(open(temp_file.name, 'r').read(),"tempfile")
        try:
            with open(temp_file.name, 'rb') as csv_file:
                from django.core.files import File

                # Save the CSV file to the converted_csv field
                instance.converted_csv.save(f'{instance.file.name}.csv', File(csv_file), save=True)
                print(instance.converted_csv)
        except Exception as e:
            print(e)
            
    elif file_type == "IMAGE":
    
        from PIL import Image
        from datetime import datetime
        import pytesseract
        import tempfile
        from django.core.files import File
        
        import csv
        pytesseract.tesseract_cmd =  "/opt/homebrew/bin/tesseract"
        print(pytesseract.image_to_string(Image.open(instance.file)))
        content = pytesseract.image_to_string(Image.open(instance.file))
        extracted_data = extract_image_data(content)
        print(extracted_data, "ect")
        csv_header = [
            'Plant', 'Order Type', 'Price grp', 'Customer', 'Customer Name',
            'City/Destination', 'Invoice No.', 'Inv. Date', 'Product Code',
            'Product Name', 'Batch No.', 'MRP', 'Billing Rate', 'Billing Quantity',
            'Taxable Amt.', 'Invoice Amt', 'Plant Name', 'Dist. Channel',
            'Price Grp Desc.', 'Customer State', 'Customer PO No.', 'PO Date',
            'System Order No.', 'Ord. Date', 'Product Type', 'Local Sales Tax NO.',
            'Central Sales Tax No.', 'Material Group3', 'Division', 'Mfg. Plant',
            'Mfg. Date', 'Exp. Date', 'Free Quantity', 'Disc.', 'Cash Disc.',
            'Tax Type', 'Tax %', 'Tax Amt.', 'Add. Tax', 'Surcharge', 'Total Tax',
            'LBT', 'Ref. Invoice No.(Returns)', 'Ref. Inv. Dt.', 'Exc. Inv. No.',
            'Exc. Inv. Dt.', 'Exc. Duty %', 'Exc. Inv. Amt.', 'Product Status',
            'Reason For Return', 'Reason For Rejection', 'Str. Loc.', 'Sales District',
            'Sales Group', 'Customer Group', 'Emp. Code', 'Employee Name',
            'C Form No.', 'HSN Code', 'Business Place', 'JOCG', 'JOSG', 'JOIG',
            'JOUG', 'PTR', 'PTS', 'Disc. %', 'Prod. Category',
            'Prod. Category Description', 'GSTIN No. of Customer', 'GST Inv. No.'
        ]
        csv_filename = f"invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode='w+', newline='', encoding='utf-8') as temp_file:
                writer = csv.DictWriter(temp_file, fieldnames=csv_header)

                # Write the header
                writer.writeheader()
                print(len([extracted_data]))
                # Write the rows
                for row in [extracted_data]:
                    writer.writerow(row)

                # Save the temporary CSV file to the Django model field
                temp_file.seek(0)
                instance.converted_csv.save(f'{instance.file.name}.csv', File(temp_file), save=True)
                print(instance.converted_csv)
        except Exception as e:
            print(e)
        finally:
            # Ensure that the temporary file is closed and removed
            if temp_file:
                temp_file.close()
                os.remove(temp_file.name)
        
        return 
        

            