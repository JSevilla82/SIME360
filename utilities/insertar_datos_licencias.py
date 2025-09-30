import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.modelos import Licencia

def insertar_licencias():

    """
    Inserta una lista predefinida de licencias en la base de datos,
    evitando duplicados basados en el LicenciaSkuId.
    """
    
    # Datos extraídos de la imagen
    licencias_a_insertar = [
        {'LicenciaSkuId': '46c3a859-c90d-40b3-9551-6178a48d5c18', 'NombreLicencia': 'Office 365 E3 (No Teams)', 'LicenciaPrincipal': 1, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '05e9a617-0261-4cee-bb44-138d3ef5d965', 'NombreLicencia': 'Office 365 E3', 'LicenciaPrincipal': 1, 'LicenciaDePago': 1},
        {'LicenciaSkuId': 'bc946dac-7877-4271-b2f7-99d2db13cd2c', 'NombreLicencia': 'Prueba de Dynamics 365 Customer Voice', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': 'a403ebcc-fae0-4ca2-8c8c-7a907fd6c235', 'NombreLicencia': 'Power BI Estandar', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': 'f30db892-07e9-47e9-837c-80727f46fd3d', 'NombreLicencia': 'Microsoft Power Automate', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': 'f8a1db68-be16-40ed-86d5-cb42e701560', 'NombreLicencia': 'Power BI Pro', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '4a51bf65-409c-4a91-b945-1121b571cc9d', 'NombreLicencia': 'Power Automate per user plan', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '53818b1b-4a27-454b-8896-0dba576410e6', 'NombreLicencia': 'Project Plan 3', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '1f2f344a-700d-42c9-9427-5cea1d5d7ba6', 'NombreLicencia': 'Prueba de Microsoft Stream', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': '99049c9c-6011-4908-bf17-15f496e6519d', 'NombreLicencia': 'OneDrive for Business (Plan 2)', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '606d54a9-78d8-4298-ad8b-df6f4481c80', 'NombreLicencia': 'Power Virtual Agents Viral Trial', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': 'dcb1a3ae-b33f-4487-846a-a640262fadf4', 'NombreLicencia': 'Microsoft Power Apps for Developer', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': '338148b6-1b11-4102-afb9-f92b6cdc0f8d', 'NombreLicencia': 'Dynamics 365 P1 Trial for Information Workers', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': 'e0dfc8b9-9531-4ec8-94b4-9fec23b05fc8', 'NombreLicencia': 'Microsoft Teams Exploratory', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': 'c1d032e0-5619-4761-9b5c-75b6831e1711', 'NombreLicencia': 'Power BI Premium por Usuario', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '3f9f06f5-3c31-472c-985f-62d9c10ec167', 'NombreLicencia': 'Power Pages vTrial for Makers', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': 'b30411f5-fea1-4a59-9ad9-3db7c7ead579', 'NombreLicencia': 'Power Apps Premium', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '52ea0e27-ae73-4983-a08f-13561ebdb823', 'NombreLicencia': 'Teams Premium (for Departments)', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '4cde982a-ede4-4409-9ae6-b003453c8ea6', 'NombreLicencia': 'Salas de Microsoft Teams Pro', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '5b631642-bd26-49fe-bd20-1daaa972ef80', 'NombreLicencia': 'Microsoft Power Apps for Developer', 'LicenciaPrincipal': 0, 'LicenciaDePago': 0},
        {'LicenciaSkuId': '7e31c0d9-9551-471d-836f-32ee72be4a01', 'NombreLicencia': 'Microsoft Teams Enterprise', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '4b244418-9658-4451-a2b8-b5e2b364e8bd', 'NombreLicencia': 'Visio Online Plan 1', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '4b585984-651b-448a-9e53-3b10f0687f7f', 'NombreLicencia': 'Office 365 F3', 'LicenciaPrincipal': 1, 'LicenciaDePago': 1},
        {'LicenciaSkuId': 'dcf0408c-aaec-446c-afd4-43e3683943ea', 'NombreLicencia': 'Office 365 E3 (No Teams)', 'LicenciaPrincipal': 1, 'LicenciaDePago': 1},
        {'LicenciaSkuId': '6fd2c87f-b296-42f0-b197-1e91e994b900', 'NombreLicencia': 'Office 365 E3', 'LicenciaPrincipal': 1, 'LicenciaDePago': 1},
        {'LicenciaSkuId': 'b4d7b828-e8dc-4518-91f9-e123ae48440d', 'NombreLicencia': 'Power Apps per app', 'LicenciaPrincipal': 0, 'LicenciaDePago': 1}
    ]

    with app.app_context():
        print("Iniciando la inserción de licencias...")
        for lic_data in licencias_a_insertar:
            existe = Licencia.query.filter_by(LicenciaSkuId=lic_data['LicenciaSkuId']).first()
            if not existe:
                nueva_licencia = Licencia(
                    LicenciaSkuId=lic_data['LicenciaSkuId'],
                    NombreLicencia=lic_data['NombreLicencia'],
                    LicenciaPrincipal=bool(lic_data['LicenciaPrincipal']),
                    LicenciaDePago=bool(lic_data['LicenciaDePago'])
                )
                db.session.add(nueva_licencia)
                print(f"  -> Insertando: {lic_data['NombreLicencia']}")
            else:
                print(f"  -- Omitiendo (ya existe): {lic_data['NombreLicencia']}")
        db.session.commit()
        print("\n¡Proceso de inserción completado!")

if __name__ == '__main__':
    insertar_licencias()



#     $SKUs = @{
#     'e4654015-5daf-4a48-9b37-4f309dddd88b'  = 'Advanced Communications'
#     'd2dea78b-507c-4e56-b400-39447f4738f8'  = 'AI Builder Capacity add-on'
#     '8f0c5670-4e56-4892-b06d-91c085d7004f'  = 'APP CONNECT IW'
#     '0c266dff-15dd-4b49-8397-2bb16070ed52'  = 'Microsoft 365 Audio Conferencing'
#     '2b9c8e7c-319c-43a2-a2a0-48c5c6161de7'  = 'AZURE ACTIVE DIRECTORY BASIC'
#     '078d2b04-f1bd-4111-bbd4-b4b1b354cef4'  = 'AZURE ACTIVE DIRECTORY PREMIUM P1'
#     '84a661c4-e949-4bd2-a560-ed7766fcaf2b'  = 'AZURE ACTIVE DIRECTORY PREMIUM P2'
#     'c52ea49f-fe5d-4e95-93ba-1de91d380f89'  = 'AZURE INFORMATION PROTECTION PLAN 1'
#     '90d8b3f8-712e-4f7b-aa1e-62e7ae6cbe96'  = 'Business Apps (free)'
#     '295a8eb0-f78d-45c7-8b5b-1eed5ed02dff'  = 'COMMON AREA PHONE'
#     'b1511558-69bd-4e1b-8270-59ca96dba0f3'  = 'Common Area Phone for GCC'
#     'e612d426-6bc3-4181-9658-91aa906b0ac0'  = 'Common Data Service Database Capacity'
#     'eddf428b-da0e-4115-accf-b29eb0b83965'  = 'Common Data Service Database Capacity for Government'
#     '448b063f-9cc6-42fc-a0e6-40e08724a395'  = 'Common Data Service Log Capacity'
#     '47794cd0-f0e5-45c5-9033-2eb6b5fc84e0'  = 'COMMUNICATIONS CREDITS'
#     '328dc228-00bc-48c6-8b09-1fbc8bc3435d'  = 'Dynamics 365 - Additional Database Storage (Qualified Offer)'
#     '9d776713-14cb-4697-a21d-9a52455c738a'  = 'Dynamics 365 - Additional Production Instance (Qualified Offer)'
#     'e06abcc2-7ec5-4a79-b08b-d9c282376f72'  = 'Dynamics 365 - Additional Non-Production Instance (Qualified Offer)'
#     'c6df1e30-1c9f-427f-907c-3d913474a1c7'  = 'Dynamics 365 AI for Market Insights (Preview)'
#     '673afb9d-d85b-40c2-914e-7bf46cd5cd75'  = 'Dynamics 365 Asset Management Addl Assets'
#     'a58f5506-b382-44d4-bfab-225b2fbf8390'  = 'Dynamics 365 Business Central Additional Environment Addon'
#     '7d0d4f9a-2686-4cb8-814c-eff3fdab6d74'  = 'Dynamics 365 Business Central Database Capacity'
#     '2880026b-2b0c-4251-8656-5d41ff11e3aa'  = 'Dynamics 365 Business Central Essentials'
#     '9a1e33ed-9697-43f3-b84c-1b0959dbb1d4'  = 'Dynamics 365 Business Central External Accountant'
#     '6a4a1628-9b9a-424d-bed5-4118f0ede3fd'  = 'Dynamics 365 Business Central for IWs'
#     'f991cecc-3f91-4cd0-a9a8-bf1c8167e029'  = 'Dynamics 365 Business Central Premium'
#     'ea126fc5-a19e-42e2-a731-da9d437bffcf'  = 'Dynamics 365 Customer Engagement Plan'
#     '1e615a51-59db-4807-9957-aa83c3657351'  = 'Dynamics 365 Customer Service Enterprise Viral Trial '
#     '61e6bd70-fbdb-4deb-82ea-912842f39431'  = 'Dynamics 365 Customer Service Insights Trial'
#     'bc946dac-7877-4271-b2f7-99d2db13cd2c'  = 'Dynamics 365 Customer Voice Trial'
#     '1439b6e2-5d59-4873-8c59-d60e2a196e92'  = 'Dynamics 365 Customer Service Professional'
#     '446a86f8-a0cb-4095-83b3-d100eb050e3d'  = 'Dynamics 365 Customer Voice Additional Responses'
#     '65f71586-ade3-4ce1-afc0-1b452eaf3782'  = 'Dynamics 365 Customer Voice Additional Responses'
#     'e2ae107b-a571-426f-9367-6d4c8f1390ba'  = 'Dynamics 365 Customer Voice USL'
#     'a4bfb28e-becc-41b0-a454-ac680dc258d3'  = 'Dynamics 365 Enterprise Edition - Additional Portal (Qualified Offer)'
#     '29fcd665-d8d1-4f34-8eed-3811e3fca7b3'  = 'Dynamics 365 Field Service Viral Trial '
#     '55c9eb4e-c746-45b4-b255-9ab6b19d5c62'  = 'Dynamics 365 Finance'
#     '749742bf-0d37-4158-a120-33567104deeb'  = 'DYNAMICS 365 FOR CUSTOMER SERVICE ENTERPRISE EDITION'
#     'cc13a803-544e-4464-b4e4-6d6169a138fa'  = 'DYNAMICS 365 FOR FINANCIALS BUSINESS EDITION'
#     '8edc2cf8-6438-4fa9-b6e3-aa1660c640cc'  = 'DYNAMICS 365 FOR SALES AND CUSTOMER SERVICE ENTERPRISE EDITION'
#     '1e1a282c-9c54-43a2-9310-98ef728faace'  = 'DYNAMICS 365 FOR SALES ENTERPRISE EDITION'
#     '238e2f8d-e429-4035-94db-6926be4ffe7b'  = 'Dynamics 365 Marketing Business Edition '
#     '7ed4877c-0863-4f69-9187-245487128d4f'  = 'Dynamics 365 Regulatory Service - Enterprise Edition Trial '
#     '6ec92958-3cc1-49db-95bd-bc6b3798df71'  = 'Dynamics 365 Sales Premium Viral Trial '
#     'be9f9771-1c64-4618-9907-244325141096'  = 'Dynamics 365 For Sales Professional'
#     '9c7bff7a-3715-4da7-88d3-07f57f8d0fb6'  = 'Dynamics 365 For Sales Professional Trial '
#     '245e6bf9-411e-481e-8611-5c08595e2988'  = 'Dynamics 365 Sales Professional Attach to Qualifying Dynamics 365 Base Offer'
#     'f2e48cb3-9da0-42cd-8464-4a54ce198ad0'  = 'DYNAMICS 365 FOR SUPPLY CHAIN MANAGEMENT'
#     '3a256e9a-15b6-4092-b0dc-82993f4debc6'  = 'Dynamics 365 for Talent'
#     'e561871f-74fa-4f02-abee-5b0ef54dd36d'  = 'Dynamics 365 Talent: Attract '
#     '8e7a3d30-d97d-43ab-837c-d7701cef83dc'  = 'DYNAMICS 365 FOR TEAM MEMBERS ENTERPRISE EDITION'
#     '0a389a77-9850-4dc4-b600-bc66fdfefc60'  = 'Dynamics 365 Guides'
#     '3bbd44ed-8a70-4c07-9088-6232ddbd5ddd'  = 'Dynamics 365 Operations - Device'
#     'e485d696-4c87-4aac-bf4a-91b2fb6f0fa7'  = 'Dynamics 365 Operations - Sandbox Tier 2:Standard Acceptance Testing'
#     'f7ad4bca-7221-452c-bdb6-3e6089f25e06'  = 'Dynamics 365 Operations - Sandbox Tier 4:Standard Performance Testing'
#     '338148b6-1b11-4102-afb9-f92b6cdc0f8d'  = 'DYNAMICS 365 P1 TRIAL FOR INFORMATION WORKERS'
#     '7a551360-26c4-4f61-84e6-ef715673e083'  = 'Dynamics 365 Remote Assist'
#     'e48328a2-8e98-4484-a70f-a99f8ac9ec89'  = 'Dynamics 365 Remote Assist HoloLens'
#     '5b22585d-1b71-4c6b-b6ec-160b1a9c2323'  = 'Dynamics 365 Sales Enterprise Attach to Qualifying Dynamics 365 Base Offer'
#     'b56e7ccc-d5c7-421f-a23b-5c18bdbad7c0'  = 'DYNAMICS 365 TALENT: ONBOARD'
#     '7ac9fe77-66b7-4e5e-9e46-10eed1cff547'  = 'DYNAMICS 365 TEAM MEMBERS'
#     'ccba3cfe-71ef-423a-bd87-b6df3dce59a9'  = 'DYNAMICS 365 UNF OPS PLAN ENT EDITION'
#     'efccb6f7-5641-4e0e-bd10-b4976e1bf68e'  = 'ENTERPRISE MOBILITY + SECURITY E3'
#     'b05e124f-c7cc-45a0-a6aa-8cf78c946968'  = 'ENTERPRISE MOBILITY + SECURITY E5'
#     'c793db86-5237-494e-9b11-dcd4877c2c8c'  = 'Enterprise Mobility + Security G3 GCC'
#     '8a180c2b-f4cf-4d44-897c-3d32acc4a60b'  = 'Enterprise Mobility + Security G5 GCC'
#     'e8ecdf70-47a8-4d39-9d15-093624b7f640'  = 'Exchange Enterprise CAL Services (EOP DLP)'
#     '4b9405b0-7788-4568-add1-99614e613b69'  = 'Exchange Online (Plan 1)'
#     'f37d5ebf-4bf1-4aa2-8fa3-50c51059e983'  = 'Exchange Online (Plan 1) for GCC'
#     '19ec0d23-8335-4cbd-94ac-6050e30712fa'  = 'EXCHANGE ONLINE (PLAN 2)'
#     'ee02fd1b-340e-4a4b-b355-4a514e4c8943'  = 'EXCHANGE ONLINE ARCHIVING FOR EXCHANGE ONLINE'
#     '90b5e015-709a-4b8b-b08e-3200f994494c'  = 'EXCHANGE ONLINE ARCHIVING FOR EXCHANGE SERVER'
#     '7fc0182e-d107-4556-8329-7caaa511197b'  = 'EXCHANGE ONLINE ESSENTIALS (ExO P1 BASED)'
#     'e8f81a67-bd96-4074-b108-cf193eb9433b'  = 'EXCHANGE ONLINE ESSENTIALS'
#     '80b2d799-d2ba-4d2a-8842-fb0d0f3a4b82'  = 'EXCHANGE ONLINE KIOSK'
#     'cb0a98a8-11bc-494c-83d9-c1b1ac65327e'  = 'EXCHANGE ONLINE POP'
#     '45a2423b-e884-448d-a831-d9e139c52d2f'  = 'Exchange Online Protection'
#     '061f9ace-7d42-4136-88ac-31dc755f143f'  = 'INTUNE'
#     'fcecd1f9-a91e-488d-a918-a96cdb6ce2b0'  = 'Microsoft Dynamics AX7 User Trial'
#     'cb2020b1-d8f6-41c0-9acd-8ff3d6d7831b'  = 'Microsoft Azure Multi-Factor Authentication'
#     '3dd6cf57-d688-4eed-ba52-9e40b5468c3e'  = 'Microsoft Defender for Office 365 (Plan 2)'
#     'b17653a4-2443-4e8c-a550-18249dda78bb'  = 'Microsoft 365 A1'
#     '4b590615-0888-425a-a965-b3bf7789848d'  = 'Microsoft 365 A3 for Faculty'
#     '7cfd9a2b-e110-4c39-bf20-c6a3f36a3121'  = 'MICROSOFT 365 A3 FOR STUDENTS'
#     '18250162-5d87-4436-a834-d795c15c80f3'  = 'Microsoft 365 A3 for students use benefit'
#     '1aa94593-ca12-4254-a738-81a5972958e8'  = 'Microsoft 365 A3 - Unattended License for students use benefit'
#     'e97c048c-37a4-45fb-ab50-922fbf07a370'  = 'Microsoft 365 A5 for Faculty'
#     '46c119d4-0379-4a9d-85e4-97c66d3f909e'  = 'MICROSOFT 365 A5 FOR STUDENTS'
#     '31d57bc7-3a05-4867-ab53-97a17835a411'  = 'Microsoft 365 A5 for students use benefit'
#     '81441ae1-0b31-4185-a6c0-32b6b84d419f'  = 'Microsoft 365 A5 without Audio Conferencing for students use benefit'
#     'cdd28e44-67e3-425e-be4c-737fab2899d3'  = 'MICROSOFT 365 APPS FOR BUSINESS'
#     'b214fe43-f5a3-4703-beeb-fa97188220fc'  = 'MICROSOFT 365 APPS FOR BUSINESS'
#     'c2273bd0-dff7-4215-9ef5-2c7bcfb06425'  = 'MICROSOFT 365 APPS FOR ENTERPRISE'
#     '12b8c807-2e20-48fc-b453-542b6ee9d171'  = 'Microsoft 365 Apps for Faculty'
#     '2d3091c7-0712-488b-b3d8-6b97bde6a1f5'  = 'MICROSOFT 365 AUDIO CONFERENCING FOR GCC'
#     '3b555118-da6a-4418-894f-7df1e2096870'  = 'MICROSOFT 365 BUSINESS BASIC'
#     'dab7782a-93b1-4074-8bb1-0e61318bea0b'  = 'MICROSOFT 365 BUSINESS BASIC'
#     'f245ecc8-75af-4f8e-b61f-27d8114de5f3'  = 'MICROSOFT 365 BUSINESS STANDARD'
#     'ac5cef5d-921b-4f97-9ef3-c99076e5470f'  = 'MICROSOFT 365 BUSINESS STANDARD - PREPAID LEGACY'
#     'cbdc14ab-d96c-4c30-b9f4-6ada7cdc1d46'  = 'MICROSOFT 365 BUSINESS PREMIUM'
#     'a6051f20-9cbc-47d2-930d-419183bf6cf1'  = 'Microsoft 365 Business Voice'
#     '08d7bce8-6e16-490e-89db-1d508e5e9609'  = 'Microsoft 365 Business Voice (US)'
#     'd52db95a-5ecb-46b6-beb0-190ab5cda4a8'  = 'Microsoft 365 Business Voice (without calling plan) '
#     '8330dae3-d349-44f7-9cad-1b23c64baabe'  = 'Microsoft 365 Business Voice (without Calling Plan) for US'
#     '11dee6af-eca8-419f-8061-6864517c1875'  = 'MICROSOFT 365 DOMESTIC CALLING PLAN (120 Minutes)'
#     '923f58ab-fca1-46a1-92f9-89fda21238a8'  = 'Microsoft 365 Domestic Calling Plan for GCC'
#     '05e9a617-0261-4cee-bb44-138d3ef5d965'  = 'MICROSOFT 365 E3'
#     'c2ac2ee4-9bb1-47e4-8541-d689c7e83371'  = 'Microsoft 365 E3 - Unattended License'
#     'd61d61cc-f992-433f-a577-5bd016037eeb'  = 'Microsoft 365 E3_USGOV_DOD'
#     'ca9d1dd9-dfe9-4fef-b97c-9bc1ea3c3658'  = 'Microsoft 365 E3_USGOV_GCCHIGH'
#     '06ebc4ee-1bb5-47dd-8120-11324bc54e06'  = 'Microsoft 365 E5'
#     '184efa21-98c3-4e5d-95ab-d07053a96e67'  = 'Microsoft 365 E5 Compliance'
#     '26124093-3d78-432b-b5dc-48bf992543d5'  = 'Microsoft 365 E5 Security'
#     '44ac31e7-2999-4304-ad94-c948886741d4'  = 'Microsoft 365 E5 Security for EMS E5'
#     'cd2925a3-5076-4233-8931-638a8c94f773'  = 'Microsoft 365 E5 without Audio Conferencing '
#     '44575883-256e-4a79-9da4-ebe9acabe2b2'  = 'Microsoft 365 F1'
#     '66b55226-6b4f-492c-910c-a3b7a3c9d993'  = 'Microsoft 365 F3'
#     '2a914830-d700-444a-b73c-e3f31980d833'  = 'Microsoft 365 F3 GCC'
#     '32b47245-eb31-44fc-b945-a8b1576c439f'  = 'Microsoft 365 F5 Security + Compliance Add-on '
#     'f30db892-07e9-47e9-837c-80727f46fd3d'  = 'MICROSOFT FLOW FREE'
#     '99cc8282-2f74-4954-83b7-c6a9a1999067'  = 'Microsoft 365 E5 Suite features'
#     '50f60901-3181-4b75-8a2c-4c8e4c1d5a72'  = 'Microsoft 365 F1'
#     'e823ca47-49c4-46b3-b38d-ca11d5abe3d2'  = 'MICROSOFT 365 G3 GCC'
#     'e43b5b99-8dfb-405f-9987-dc307f34bcbd'  = 'MICROSOFT 365 PHONE SYSTEM'
#     'd01d9287-694b-44f3-bcc5-ada78c8d953e'  = 'MICROSOFT 365 PHONE SYSTEM FOR DOD'
#     'd979703c-028d-4de5-acbf-7955566b69b9'  = 'MICROSOFT 365 PHONE SYSTEM FOR FACULTY'
#     'a460366a-ade7-4791-b581-9fbff1bdaa85'  = 'MICROSOFT 365 PHONE SYSTEM FOR GCC'
#     '7035277a-5e49-4abc-a24f-0ec49c501bb5'  = 'MICROSOFT 365 PHONE SYSTEM FOR GCCHIGH'
#     'aa6791d3-bb09-4bc2-afed-c30c3fe26032'  = 'MICROSOFT 365 PHONE SYSTEM FOR SMALL AND MEDIUM BUSINESS'
#     '1f338bbc-767e-4a1e-a2d4-b73207cc5b93'  = 'MICROSOFT 365 PHONE SYSTEM FOR STUDENTS'
#     'ffaf2d68-1c95-4eb3-9ddd-59b81fba0f61'  = 'MICROSOFT 365 PHONE SYSTEM FOR TELSTRA'
#     'b0e7de67-e503-4934-b729-53d595ba5cd1'  = 'MICROSOFT 365 PHONE SYSTEM_USGOV_DOD'
#     '985fcb26-7b94-475b-b512-89356697be71'  = 'MICROSOFT 365 PHONE SYSTEM_USGOV_GCCHIGH'
#     '440eaaa8-b3e0-484b-a8be-62870b9ba70a'  = 'MICROSOFT 365 PHONE SYSTEM - VIRTUAL USER'
#     '2cf22bcb-0c9e-4bc6-8daf-7e7654c0f285'  = 'Microsoft 365 Phone System - Virtual User for GCC'
#     '2347355b-4e81-41a4-9c22-55057a399791'  = 'Microsoft 365 Security and Compliance for Firstline Workers'
#     '726a0894-2c77-4d65-99da-9775ef05aad1'  = 'MICROSOFT BUSINESS CENTER'
#     'df845ce7-05f9-4894-b5f2-11bbfbcfd2b6'  = 'Microsoft Cloud App Security'
#     '111046dd-295b-4d6d-9724-d52ac90bd1f2'  = 'MICROSOFT DEFENDER FOR ENDPOINT'
#     '509e8ab6-0274-4cda-bcbd-bd164fd562c4'  = 'Microsoft Defender for Endpoint Server'
#     '906af65a-2970-46d5-9b58-4e9aa50f0657'  = 'MICROSOFT DYNAMICS CRM ONLINE BASIC'
#     '98defdf7-f6c1-44f5-a1f6-943b6764e7a5'  = 'Microsoft Defender for Identity'
#     'd0d1ca43-b81a-4f51-81e5-a5b1ad7bb005'  = 'Microsoft Defender for Office 365 (Plan 1) GCC '
#     '56a59ffb-9df1-421b-9e61-8b568583474d'  = 'Microsoft Defender for Office 365 (Plan 2) GCC'
#     'd17b27af-3f49-4822-99f9-56a661538792'  = 'MICROSOFT DYNAMICS CRM ONLINE'
#     'ba9a34de-4489-469d-879c-0f0f145321cd'  = 'MS IMAGINE ACADEMY'
#     '2b317a4a-77a6-4188-9437-b68a77b4e2c6'  = 'Microsoft Intune Device'
#     '2c21e77a-e0d6-4570-b38a-7ff2dc17d2ca'  = 'MICROSOFT INTUNE DEVICE FOR GOVERNMENT'
#     '5b631642-bd26-49fe-bd20-1daaa972ef80'  = 'Microsoft Power Apps for Developer '
#     'dcb1a3ae-b33f-4487-846a-a640262fadf4'  = 'Microsoft Power Apps Plan 2 Trial'
#     '4755df59-3f73-41ab-a249-596ad72b5504'  = 'MICROSOFT POWER AUTOMATE PLAN 2'
#     'e6025b08-2fa5-4313-bd0a-7e5ffca32958'  = 'MICROSOFT INTUNE SMB'
#     'ddfae3e3-fcb2-4174-8ebd-3023cb213c8b'  = 'Microsoft Power Apps Plan 2 (Qualified Offer)'
#     '1f2f344a-700d-42c9-9427-5cea1d5d7ba6'  = 'MICROSOFT STREAM'
#     'ec156933-b85b-4c50-84ec-c9e5603709ef'  = 'Microsoft Stream Plan 2'
#     '9bd7c846-9556-4453-a542-191d527209e8'  = 'Microsoft Stream Storage Add-On (500 GB)'
#     '16ddbbfc-09ea-4de2-b1d7-312db6112d70'  = 'MICROSOFT TEAMS (FREE)'
#     '710779e8-3d4a-4c88-adb9-386c958d1fdf'  = 'MICROSOFT TEAMS EXPLORATORY'
#     '6070a4c8-34c6-4937-8dfb-39bbc6397a60'  = 'Microsoft Teams Rooms Standard'
#     '74fbf1bb-47c6-4796-9623-77dc7371723b'  = 'Microsoft Teams Trial'
#     '9fa2f157-c8e4-4351-a3f2-ffa506da1406'  = 'Microsoft Threat Experts - Experts on Demand'
#     '84951599-62b7-46f3-9c9d-30551b2ad607'  = 'Multi-Geo Capabilities in Office 365'
#     'aa2695c9-8d59-4800-9dc8-12e01f1735af'  = 'Nonprofit Portal'
#     '4fb214cb-a430-4a91-9c91-4976763aa78f'  = 'Teams Rooms Premium'
#     '94763226-9b3c-4e75-a931-5c89701abe66'  = 'Office 365 A1 for faculty'
#     '78e66a63-337a-4a9a-8959-41c6654dfb56'  = 'Office 365 A1 Plus for faculty'
#     '314c4481-f395-4525-be8b-2ec4bb1e9d91'  = 'Office 365 A1 for students '
#     'e82ae690-a2d5-4d76-8d30-7c6e01e6022e'  = 'Office 365 A1 Plus for students'
#     'e578b273-6db4-4691-bba0-8d691f4da603'  = 'Office 365 A3 for faculty'
#     '98b6e773-24d4-4c0d-a968-6e787a1f8204'  = 'Office 365 A3 for students'
#     'a4585165-0533-458a-97e3-c400570268c4'  = 'Office 365 A5 for faculty'
#     'ee656612-49fa-43e5-b67e-cb1fdf7699df'  = 'Office 365 A5 for students'
#     '1b1b1f7a-8355-43b6-829f-336cfccb744c'  = 'Office 365 Advanced Compliance'
#     '1a585bba-1ce3-416e-b1d6-9c482b52fcf6'  = 'Office 365 Advanced Compliance for GCC'
#     '4ef96642-f096-40de-a3e9-d83fb2f90211'  = 'Microsoft Defender for Office 365 (Plan 1)'
#     'e5788282-6381-469f-84f0-3d7d4021d34d'  = 'Office 365 Extra File Storage for GCC'
#     '29a2f828-8f39-4837-b8ff-c957e86abe3c'  = 'Microsoft Teams Commercial Cloud'
#     '84d5f90f-cd0d-4864-b90b-1c7ba63b4808'  = 'Office 365 Cloud App Security'
#     '99049c9c-6011-4908-bf17-15f496e6519d'  = 'Office 365 Extra File Storage'
#     '18181a46-0d4e-45cd-891e-60aabd171b4e'  = 'OFFICE 365 E1'
#     '6634e0ce-1a9f-428c-a498-f84ec7b8aa2e'  = 'OFFICE 365 E2'
#     '6fd2c87f-b296-42f0-b197-1e91e994b900'  = 'Office 365 E3'
#     '189a915c-fe4f-4ffa-bde4-85b9628d07a0'  = 'OFFICE 365 E3 DEVELOPER'
#     'b107e5a3-3e60-4c0d-a184-a7e4395eb44c'  = 'Office 365 E3_USGOV_DOD'
#     'aea38a85-9bd5-4981-aa00-616b411205bf'  = 'Office 365 E3_USGOV_GCCHIGH'
#     '1392051d-0cb9-4b7a-88d5-621fee5e8711'  = 'OFFICE 365 E4'
#     'c7df2760-2c81-4ef7-b578-5b5392b571df'  = 'Office 365 E5'
#     '26d45bd9-adf1-46cd-a9e1-51e9a5524128'  = 'OFFICE 365 E5 WITHOUT AUDIO CONFERENCING'
#     '4b585984-651b-448a-9e53-3b10f069cf7f'  = 'OFFICE 365 F3'
#     '3f4babde-90ec-47c6-995d-d223749065d1'  = 'Office 365 G1 GCC'
#     '535a3a29-c5f0-42fe-8215-d3b9e1f38c4a'  = 'OFFICE 365 G3 GCC'
#     '8900a2c0-edba-4079-bdf3-b276e293b6a8'  = 'Office 365 G5 GCC'
#     '04a7fb0d-32e0-4241-b4f5-3f7618cd1162'  = 'OFFICE 365 MIDSIZE BUSINESS'
#     'bd09678e-b83c-4d3f-aaba-3dad4abd128b'  = 'OFFICE 365 SMALL BUSINESS'
#     'fc14ec4a-4169-49a4-a51e-2c852931814b'  = 'OFFICE 365 SMALL BUSINESS PREMIUM'
#     'e6778190-713e-4e4f-9119-8b8238de25df'  = 'ONEDRIVE FOR BUSINESS (PLAN 1)'
#     'ed01faf2-1d88-4947-ae91-45ca18703a96'  = 'ONEDRIVE FOR BUSINESS (PLAN 2)'
#     '87bbbc60-4754-4998-8c88-227dca264858'  = 'POWERAPPS AND LOGIC FLOWS'
#     'bf666882-9c9b-4b2e-aa2f-4789b0a52ba2'  = 'PowerApps per app baseline access'
#     'a8ad7d2b-b8cf-49d6-b25a-69094a0be206'  = 'Power Apps per app plan'
#     'b30411f5-fea1-4a59-9ad9-3db7c7ead579'  = 'Power Apps per user plan'
#     '8e4c6baa-f2ff-4884-9c38-93785d0d7ba1'  = 'Power Apps per user plan for Government'
#     'eca22b68-b31f-4e9c-a20c-4d40287bc5dd'  = 'PowerApps Plan 1 for Government'
#     '26c903d5-d385-4cb1-b650-8d81a643b3c4'  = 'Power Apps Portals login capacity add-on Tier 2 (10 unit min) for Government'
#     '15a64d3e-5b99-4c4b-ae8f-aa6da264bfe7'  = 'Power Apps Portals page view capacity add-on for Government'
#     'b3a42176-0a8c-4c3f-ba4e-f2b37fe5be6b'  = 'Power Automate per flow plan'
#     '4a51bf65-409c-4a91-b845-1121b571cc9d'  = 'Power Automate per user plan'
#     'd80a4c5d-8f05-4b64-9926-6574b9e6aee4'  = 'Power Automate per user plan dept'
#     'c8803586-c136-479a-8ff3-f5f32d23a68e'  = 'Power Automate per user plan for Government'
#     'eda1941c-3c4f-4995-b5eb-e85a42175ab9'  = 'Power Automate per user with attended RPA plan'
#     '3539d28c-6e35-4a30-b3a9-cd43d5d3e0e2'  = 'Power Automate unattended RPA add-on'
#     'e2767865-c3c9-4f09-9f99-6eee6eef861a'  = 'Power BI'
#     'a403ebcc-fae0-4ca2-8c8c-7a907fd6c235'  = 'Power BI (free)'
#     '45bc2c81-6072-436a-9b0b-3b12eefbc402'  = 'POWER BI FOR OFFICE 365 ADD-ON'
#     '7b26f5ab-a763-4c00-a1ac-f6c4b5506945'  = 'Power BI Premium P1'
#     'c1d032e0-5619-4761-9b5c-75b6831e1711'  = 'Power BI Premium Per User'
#     'de376a03-6e5b-42ec-855f-093fb50b8ca5'  = 'Power BI Premium Per User Add-On'
#     'f168a3fb-7bcf-4a27-98c3-c235ea4b78b4'  = 'Power BI Premium Per User Dept'
#     'f8a1db68-be16-40ed-86d5-cb42ce701560'  = 'Power BI Pro'
#     '420af87e-8177-4146-a780-3786adaffbca'  = 'Power BI Pro CE'
#     '3a6a908c-09c5-406a-8170-8ebb63c42882'  = 'Power BI Pro Dept'
#     'f0612879-44ea-47fb-baf0-3d76d9235576'  = 'Power BI Pro for GCC'
#     'e4e55366-9635-46f4-a907-fc8c3b5ec81f'  = 'Power Virtual Agent'
#     '606b54a9-78d8-4298-ad8b-df6ef4481c80'  = 'Power Virtual Agents Viral Trial'
#     'a10d5e58-74da-4312-95c8-76be4e5b75a0'  = 'PROJECT FOR OFFICE 365'
#     '776df282-9fc0-4862-99e2-70e561b9909e'  = 'Project Online Essentials'
#     'ca1a159a-f09e-42b8-bb82-cb6420f54c8e'  = 'Project Online Essentials for GCC'
#     '09015f9f-377f-4538-bbb5-f75ceb09358a'  = 'PROJECT ONLINE PREMIUM'
#     '2db84718-652c-47a7-860c-f10d8abbdae3'  = 'PROJECT ONLINE PREMIUM WITHOUT PROJECT CLIENT'
#     'f82a60b8-1ee3-4cfb-a4fe-1c6a53c2656c'  = 'PROJECT ONLINE WITH PROJECT FOR OFFICE 365'
#     'beb6439c-caad-48d3-bf46-0c82871e12be'  = 'PROJECT PLAN 1'
#     '84cd610f-a3f8-4beb-84ab-d9d2c902c6c9'  = 'Project Plan 1 (for Department)'
#     '53818b1b-4a27-454b-8896-0dba576410e6'  = 'Project Plan 3'
#     '46102f44-d912-47e7-b0ca-1bd7b70ada3b'  = 'Project Plan 3 (for Department)'
#     '074c6829-b3a0-430a-ba3d-aca365e57065'  = 'Project Plan 3 for GCC'
#     'f2230877-72be-4fec-b1ba-7156d6f75bd6'  = 'Project Plan 5 for GCC'
#     '8c4ce438-32a7-4ac5-91a6-e22ae08d9c8b'  = 'Rights Management Adhoc'
#     '093e8d14-a334-43d9-93e3-30589a8b47d0'  = 'Rights Management Service Basic Content Protection'
#     '08e18479-4483-4f70-8f17-6f92156d8ea9'  = 'Sensor Data Intelligence Additional Machines Add-in for Dynamics 365 Supply Chain Management'
#     '9ea4bdef-a20b-4668-b4a7-73e1f7696e0a'  = 'Sensor Data Intelligence Scenario Add-in for Dynamics 365 Supply Chain Management'
#     '1fc08a02-8b3d-43b9-831e-f76859e04e1a'  = 'SHAREPOINT ONLINE (PLAN 1)'
#     'a9732ec9-17d9-494c-a51c-d6b45b384dcb'  = 'SHAREPOINT ONLINE (PLAN 2)'
#     'f61d4aba-134f-44e9-a2a0-f81a5adb26e4'  = 'SharePoint Syntex'
#     'b8b749f8-a4ef-4887-9539-c95b1eaa5db7'  = 'SKYPE FOR BUSINESS ONLINE (PLAN 1)'
#     'd42c793f-6c78-4f43-92ca-e8f6a02b035f'  = 'SKYPE FOR BUSINESS ONLINE (PLAN 2)'
#     'd3b4fe1f-9992-4930-8acb-ca6ec609365e'  = 'SKYPE FOR BUSINESS PSTN DOMESTIC AND INTERNATIONAL CALLING'
#     '0dab259f-bf13-4952-b7f8-7db8f131b28d'  = 'SKYPE FOR BUSINESS PSTN DOMESTIC CALLING'
#     '54a152dc-90de-4996-93d2-bc47e670fc06'  = 'SKYPE FOR BUSINESS PSTN DOMESTIC CALLING (120 Minutes)'
#     '06b48c5f-01d9-4b18-9015-03b52040f51a'  = 'Skype for Business PSTN Usage Calling Plan'
#     'de3312e1-c7b0-46e6-a7c3-a515ff90bc86'  = 'TELSTRA CALLING FOR O365'
#     '9f3d9c1d-25a5-4aaa-8e59-23a1e6450a67'  = 'Universal Print'
#     'ca7f3140-d88c-455b-9a1c-7f0679e31a76'  = 'Visio Plan 1'
#     '38b434d2-a15e-4cde-9a98-e737c75623e1'  = 'Visio Plan 2'
#     '4b244418-9658-4451-a2b8-b5e2b364e9bd'  = 'VISIO ONLINE PLAN 1'
#     'c5928f49-12ba-48f7-ada3-0d743a3601d5'  = 'VISIO ONLINE PLAN 2'
#     '4ae99959-6b0f-43b0-b1ce-68146001bdba'  = 'VISIO PLAN 2 FOR GCC'
#     '4016f256-b063-4864-816e-d818aad600c9'  = 'Viva Topics'
#     '1e7e1070-8ccb-4aca-b470-d7cb538cb07e'  = 'Windows 10/11 Enterprise E5 (Original)'
#     '8efbe2f6-106e-442f-97d4-a59aa6037e06'  = 'Windows 10 Enterprise A3 for faculty'
#     'd4ef921e-840b-4b48-9a90-ab6698bc7b31'  = 'Windows 10 Enterprise A3 for students'
#     'cb10e6cd-9da4-4992-867b-67546b1db821'  = 'WINDOWS 10 ENTERPRISE E3'
#     '6a0f6da5-0b87-4190-a6ae-9bb5a2b9546a'  = 'WINDOWS 10 ENTERPRISE E3'
#     '488ba24a-39a9-4473-8ee5-19291e71b002'  = 'Windows 10 Enterprise E5'
#     '938fd547-d794-42a4-996c-1cc206619580'  = 'Windows 10 Enterprise E5 Commercial (GCC Compatible)'
#     '42e6818f-8966-444b-b7ac-0027c83fa8b5'  = 'Windows 365 Business 2 vCPU 4 GB 64 GB'
#     '439ac253-bfbc-49c7-acc0-6b951407b5ef'  = 'Windows 365 Business 4 vCPU 16 GB 128 GB (with Windows Hybrid Benefit)'
#     '7bb14422-3b90-4389-a7be-f1b745fc037f'  = 'Windows 365 Enterprise 2 vCPU 4 GB 64 GB'
#     '6470687e-a428-4b7a-bef2-8a291ad947c9'  = 'WINDOWS STORE FOR BUSINESS'
#     'c7e9d9e6-1981-4bf3-bb50-a5bdfaa06fb2'  = 'Windows Store for Business EDU Faculty'
#     '3d957427-ecdc-4df2-aacd-01cc9d519da8'  = 'Microsoft Workplace Analytics'
# }