from app.db import db
from app.models import Client, Document
from flask import request
from sqlalchemy.orm import joinedload
import base64

def register_routes(bp):

    @bp.route('/clients', methods=['GET'])
    def get_clients():
        clients = db.session.query(Client).all()

        clients = map(lambda client: {
            "id": client.id,
            "company_name": client.company_name,
            "representative_name": client.representative_name,
            "rfc": client.rfc,
            "email": client.email,
            "phone_number": client.phone_number,
        }, clients)
        clients = list(clients)
        return clients, 200
    
    @bp.route('/clients/<int:client_id>')
    def get_client(client_id=None):
        # Method 1: Select specific columns from each table
        result = db.session.query(Client).filter(Client.id == client_id).first()

        if result:
            # Build response from selected columns
            response = {
                "id": result.id,
                "company_name": result.company_name,
                "representative_name": result.representative_name,
                "rfc": result.rfc,
                "email": result.email,
                "phone_number": result.phone_number,
                "document_id": result.document.id
            }
            
            # Add document info if it exists
            if result.document:
                response["document"] = {
                    "id": result.document.id,
                    "filename": result.document.document_filename,
                    "mimetype": result.document.document_mimetype
                    # Size not included since we didn't fetch document_data
                }
            else:
                response["document"] = None
                
            return response
            
        return {"message": "Client not found"}, 404
    @bp.route('/clients/<int:client_id>/document', methods=['GET'])
    def get_client_document(client_id):
        document = db.session.query(Document).filter(Document.client_id == client_id).first()
        if document:
            # Return document data as base64 string
            document_data_base64 = base64.b64encode(document.document_data).decode('utf-8')
            return {
                "id": document.id,
                "data": document_data_base64,
                "filename": document.document_filename,
                "mimetype": document.document_mimetype
            }, 200
        return {"message": "Document not found"}, 404

    @bp.route('/clients', methods=['POST'])
    def add_client():
        data = request.get_json()        

        # print(f"Received data: {data}")

        if not data:
            return {"message": "Invalid input"}, 400
        
        try:
            new_client = Client(
                company_name=data.get("company_name"),
                representative_name=data.get("representative_name"),
                rfc=data.get("rfc"),
                email=data.get("email"),
                phone_number=data.get("phone_number")        
            )
                        
            db.session.add(new_client)
            db.session.flush()

            # Get base64 document data from JSON
            document_base64 = data.get("document")['data']  # base64 string or data URL
            document_filename = data.get("document")['filename']
            document_mimetype = data.get("document")['mimetype']

            # print(f'Base64 data: {document_base64}')
            
            if not document_base64 or not document_filename:
                return {"message": "Missing document data or filename"}, 400
            
            try:
                # Handle data URLs (e.g., "data:image/png;base64,iVBORw0KGgo...")
                if document_base64.startswith('data:'):
                    header, base64_data = document_base64.split(',', 1)
                    # Extract mimetype from data URL if not provided
                    if not document_mimetype:
                        document_mimetype = header.split(':')[1].split(';')[0]
                else:
                    base64_data = document_base64
                
                # Convert base64 to binary data (blob)
                document_binary = base64.b64decode(base64_data)
                
            except Exception as decode_error:
                return {"message": f"Invalid base64 data: {str(decode_error)}"}, 400
            
            new_document = Document(
                document_data=document_binary,  # Binary data (blob)
                document_filename=document_filename,
                document_mimetype=document_mimetype or "application/octet-stream",
                client_id=new_client.id
            )

            db.session.add(new_document)
            db.session.flush()
                        
            new_client.document_id = new_document.id
            
            # Commit all changes
            db.session.commit()

            return {"message": "Cliente agregado", "id": new_client.id}, 201
                
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error creando cliente: {str(e)}"}, 500

    @bp.route('/clients/<int:client_id>', methods=['PUT'])
    def update_client(client_id):
        data = request.get_json()
        if not data:
            return {"message": "Invalid input"}, 400

        # Method 1: Query full objects to get separate variables
        result = db.session.query(Client)\
            .filter(Client.id == client_id)\
            .first()
            
        if not result:
            return {"message": "Client not found"}, 404                    
        
        # Now you can work with both objects separately
        print(f"Working with client: {result.company_name}")
        if result.document:
            print(f"Client has document: {result.document.document_filename}")
        else:
            print("Client has no document")

        try:
            # Update client fields
            result.company_name = data.get("companyName", result.company_name)
            result.representative_name = data.get("representativeName", result.representative_name)
            result.rfc = data.get("rfc", result.rfc)
            result.email = data.get("email", result.email)
            result.phone_number = data.get("phoneNumber", result.phone_number)

            # You can also update document if needed
            if result.document and "document" in data and "data" in data["document"]:
                blob_data = base64.b64decode(data["document"].get("data", ""))
                result.document.document_data = blob_data
                result.document.document_filename = data["document"].get("filename", result.document.document_filename)
                result.document.document_mimetype = data["document"].get("mimetype", result.document.document_mimetype)

            db.session.commit()
            return {"message": "Client updated successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating client: {str(e)}"}, 500

    @bp.route('/clients/<int:client_id>', methods=['DELETE'])
    def delete_client(client_id):
        client = Client.query.get(client_id)
        if not client:
            return {"message": "Client not found"}, 404        

        try:
            db.session.delete(client)
            db.session.commit()
            return {"message": "Client deleted successfully"}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error deleting client: {str(e)}"}, 500
