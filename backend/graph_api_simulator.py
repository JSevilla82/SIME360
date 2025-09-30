# SIME_360/backend/graph_api_simulator.py
# -*- coding: utf-8 -*-
"""
Este módulo simula las respuestas de la API de Microsoft Graph utilizando 
datos estáticos y ficticios para el desarrollo y las pruebas.

Versión Corregida y Ampliada v5 (Final):
- Se garantiza que al menos 3 usuarios siempre aparezcan sin actividad en los
  informes, modificando sus perfiles base.
- Lógica de almacenamiento de Outlook y OneDrive ajustada para generar datos
  variables y reducir la cantidad de informes con uso en cero.
- Se ha hecho variable el almacenamiento asignado en los sitios de SharePoint
  para permitir la visualización de estados (verde, amarillo, rojo) según
  el porcentaje de uso.
- Se agregó la generación de datos de duración de Audio y Video para Teams.
- Se corrigió la lógica de informes de SharePoint para mostrar siempre la lista
  completa de sitios.
- Se ajustó la generación de informes de uso para incluir siempre a todos los
  usuarios, mostrando métricas de actividad en cero para los inactivos.
"""
from datetime import datetime, timedelta
import random
import uuid

# Se establece una fecha "actual" fija para que los datos generados sean consistentes
SIMULATION_TODAY = datetime(2025, 8, 24)

# ==============================================================================
# 📦 DATOS DE LICENCIAS DEL TENANT
# ==============================================================================
licencias_disponibles_object = {
    "value": [
        {"skuId": "1f2f344a-700d-42c9-9427-5cea1d5d7ba6", "skuPartNumber": "STREAM", "prepaidUnits": {"enabled": 1000000}},
        {"skuId": "46c3a859-c90d-40b3-9551-6178a48d5c18", "skuPartNumber": "Office_365_E3_(no_Teams)", "prepaidUnits": {"enabled": 19}},
        {"skuId": "4a51bf65-409c-4a91-b845-1121b571cc9d", "skuPartNumber": "FLOW_PER_USER", "prepaidUnits": {"enabled": 5}},
        {"skuId": "f8a1db68-be16-40ed-86d5-cb42ce701560", "skuPartNumber": "POWER_BI_PRO", "prepaidUnits": {"enabled": 6}},
        {"skuId": "6470687e-a428-4b7a-bef2-8a291ad947c9", "skuPartNumber": "WINDOWS_STORE", "prepaidUnits": {"enabled": 0}},
        {"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900", "skuPartNumber": "ENTERPRISEPACK", "prepaidUnits": {"enabled": 510}},
        {"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f", "skuPartNumber": "DESKLESSPACK", "prepaidUnits": {"enabled": 836}},
        {"skuId": "dcf0408c-aaec-446c-afd4-43e3683943ea", "skuPartNumber": "Microsoft_365_E3_(no_Teams)", "prepaidUnits": {"enabled": 1}},
        {"skuId": "f30db892-07e9-47e9-837c-80727f46fd3d", "skuPartNumber": "FLOW_FREE", "prepaidUnits": {"enabled": 10000}},
        {"skuId": "99049c9c-6011-4908-bf17-15f496e6519d", "skuPartNumber": "SHAREPOINTSTORAGE", "prepaidUnits": {"enabled": 2000}},
        {"skuId": "606b54a9-78d8-42c9-ad8b-df6ef4481c80", "skuPartNumber": "CCIBOTS_PRIVPREV_VIRAL", "prepaidUnits": {"enabled": 10000}},
        {"skuId": "bc946dac-7877-4271-b2f7-99d2db13cd2c", "skuPartNumber": "FORMS_PRO", "prepaidUnits": {"enabled": 1000000}},
        {"skuId": "dcb1a3ae-b33f-4487-846a-a640262fadf4", "skuPartNumber": "POWERAPPS_VIRAL", "prepaidUnits": {"enabled": 10000}},
        {"skuId": "338148b6-1b11-4102-afb9-f92b6cdc0f8d", "skuPartNumber": "DYN365_ENTERPRISE_P1_IW", "prepaidUnits": {"enabled": 10000}},
        {"skuId": "e0dfc8b9-9531-4ec8-94b4-9fec23b05fc8", "skuPartNumber": "Microsoft_Teams_Exploratory_Dept", "prepaidUnits": {"enabled": 1}},
        {"skuId": "a403ebcc-fae0-4ca2-8c8c-7a907fd6c235", "skuPartNumber": "POWER_BI_STANDARD", "prepaidUnits": {"enabled": 1000000}},
        {"skuId": "7e31c0d9-9551-471d-836f-32ee72be4a01", "skuPartNumber": "Microsoft_Teams_Enterprise_New", "prepaidUnits": {"enabled": 20}},
        {"skuId": "c1d032e0-5619-4761-9b5c-75b6831e1711", "skuPartNumber": "PBI_PREMIUM_PER_USER", "prepaidUnits": {"enabled": 5}},
        {"skuId": "3f9f06f5-3c31-472c-985f-62d9c10ec167", "skuPartNumber": "Power_Pages_vTrial_for_Makers", "prepaidUnits": {"enabled": 10000}},
        {"skuId": "4b244418-9658-4451-a2b8-b5e2b364e9bd", "skuPartNumber": "VISIOONLINE_PLAN1", "prepaidUnits": {"enabled": 1}},
        {"skuId": "53818b1b-4a27-454b-8896-0dba576410e6", "skuPartNumber": "PROJECTPROFESSIONAL", "prepaidUnits": {"enabled": 20}},
        {"skuId": "52ea0e27-ae73-4983-a08f-13561ebdb823", "skuPartNumber": "Teams_Premium_(for_Departments)", "prepaidUnits": {"enabled": 0, "suspended": 6}},
        {"skuId": "b4d7b828-e8dc-4518-91f9-e123ae48440d", "skuPartNumber": "POWERAPPS_PER_APP_NEW", "prepaidUnits": {"enabled": 1}},
        {"skuId": "4cde982a-ede4-4409-9ae6-b003453c8ea6", "skuPartNumber": "Microsoft_Teams_Rooms_Pro", "prepaidUnits": {"enabled": 3}},
        {"skuId": "5b631642-bd26-49fe-bd20-1daaa972ef80", "skuPartNumber": "POWERAPPS_DEV", "prepaidUnits": {"enabled": 10000}},
        {"skuId": "46102f44-d912-47e7-b0ca-1bd7b70ada3b", "skuPartNumber": "PROJECT_PLAN3_DEPT", "prepaidUnits": {"enabled": 0, "suspended": 2}}
    ]
}

# ==============================================================================
# 👤 PERFILES DE USUARIOS FICTICIOS (40 Usuarios con perfiles de almacenamiento)
# ==============================================================================
USER_PROFILES = [
    {"id": "11111111-aaaa-bbbb-cccc-111111111111", "displayName": "Ana Gómez (Marketing)", "mail": "ana.gomez@empresa.com.co", "jobTitle": "Gerente de Marketing", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=730)).isoformat() + "Z", "lastSignInDaysAgo": 1, "activity_level": "alta", "storage_usage": "high", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}, {"skuId": "f8a1db68-be16-40ed-86d5-cb42ce701560"}]},
    {"id": "22222222-aaaa-bbbb-cccc-222222222222", "displayName": "Carlos Rivera (Ventas)", "mail": "carlos.rivera@empresa.com.co", "jobTitle": "Ejecutivo de Ventas", "officeLocation": "Medellín", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=400)).isoformat() + "Z", "lastSignInDaysAgo": 5, "activity_level": "media", "storage_usage": "low", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}]},
    {"id": "33333333-aaaa-bbbb-cccc-333333333333", "displayName": "Beatriz Durán (RRHH)", "mail": "beatriz.duran@empresa.com.co", "jobTitle": "Analista de RRHH", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=900)).isoformat() + "Z", "lastSignInDaysAgo": 15, "activity_level": "baja", "storage_usage": "medium", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "44444444-aaaa-bbbb-cccc-444444444444", "displayName": "David Mendoza (IT)", "mail": "david.mendoza@empresa.com.co", "jobTitle": "Desarrollador Senior", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=1200)).isoformat() + "Z", "lastSignInDaysAgo": 0, "activity_level": "muy_alta", "storage_usage": "medium", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}, {"skuId": "53818b1b-4a27-454b-8896-0dba576410e6"}]},
    {"id": "55555555-aaaa-bbbb-cccc-555555555555", "displayName": "Elena Navarro (Finanzas)", "mail": "elena.navarro@empresa.com.co", "jobTitle": "Contadora", "officeLocation": "Cali", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=600)).isoformat() + "Z", "lastSignInDaysAgo": 25, "activity_level": "media", "storage_usage": "high", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "66666666-aaaa-bbbb-cccc-666666666666", "displayName": "Fernando Vega (Operaciones)", "mail": "fernando.vega@empresa.com.co", "jobTitle": "Coordinador de Logística", "officeLocation": "Barranquilla", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=800)).isoformat() + "Z", "lastSignInDaysAgo": 45, "activity_level": "baja", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "77777777-aaaa-bbbb-cccc-777777777777", "displayName": "Gabriela Torres (Nuevo Ingreso)", "mail": "gabriela.torres@empresa.com.co", "jobTitle": "Practicante", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=2)).isoformat() + "Z", "lastSignInDaysAgo": None, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": []},
    {"id": "88888888-aaaa-bbbb-cccc-888888888888", "displayName": "Héctor Castillo (Proyectos)", "mail": "hector.castillo@empresa.com.co", "jobTitle": "Líder de Proyectos", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=550)).isoformat() + "Z", "lastSignInDaysAgo": 2, "activity_level": "alta", "storage_usage": "medium", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}, {"skuId": "53818b1b-4a27-454b-8896-0dba576410e6"}]},
    {"id": "99999999-aaaa-bbbb-cccc-999999999999", "displayName": "Isabel Romero (Legal - Inactiva)", "mail": "isabel.romero@empresa.com.co", "jobTitle": "Abogada", "officeLocation": "Bogotá", "accountEnabled": False, "createdDateTime": (SIMULATION_TODAY - timedelta(days=1500)).isoformat() + "Z", "lastSignInDaysAgo": 95, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}]},
    
    # ### MODIFICADO: Usuario configurado para garantizar 'Sin Actividad' ###
    {"id": "10101010-aaaa-bbbb-cccc-101010101010", "displayName": "Javier Ponce (Sin Actividad)", "mail": "javier.ponce@empresa.com.co", "jobTitle": "Consultor Externo", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=300)).isoformat() + "Z", "lastSignInDaysAgo": 120, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    
    {"id": "11101110-aaaa-bbbb-cccc-111011101110", "displayName": "Laura Jiménez (Diseño)", "mail": "laura.jimenez@empresa.com.co", "jobTitle": "Diseñadora UX/UI", "officeLocation": "Medellín", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=500)).isoformat() + "Z", "lastSignInDaysAgo": 3, "activity_level": "alta", "storage_usage": "high", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}, {"skuId": "a403ebcc-fae0-4ca2-8c8c-7a907fd6c235"}]},
    {"id": "12121212-aaaa-bbbb-cccc-121212121212", "displayName": "Mario Vargas (Soporte)", "mail": "mario.vargas@empresa.com.co", "jobTitle": "Técnico de Soporte", "officeLocation": "Cali", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=100)).isoformat() + "Z", "lastSignInDaysAgo": 8, "activity_level": "media", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "13131313-aaaa-bbbb-cccc-131313131313", "displayName": "Natalia Rojas (Calidad)", "mail": "natalia.rojas@empresa.com.co", "jobTitle": "Auditora de Calidad", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=1100)).isoformat() + "Z", "lastSignInDaysAgo": 35, "activity_level": "baja", "storage_usage": "medium", "assignedLicenses": [{"skuId": "46c3a859-c90d-40b3-9551-6178a48d5c18"}, {"skuId": "7e31c0d9-9551-471d-836f-32ee72be4a01"}]},
    {"id": "14141414-aaaa-bbbb-cccc-141414141414", "displayName": "Óscar Perea (Innovación)", "mail": "oscar.perea@empresa.com.co", "jobTitle": "Líder de Innovación", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=250)).isoformat() + "Z", "lastSignInDaysAgo": 1, "activity_level": "muy_alta", "storage_usage": "medium", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}, {"skuId": "f8a1db68-be16-40ed-86d5-cb42ce701560"}, {"skuId": "4a51bf65-409c-4a91-b845-1121b571cc9d"}]},
    {"id": "15151515-aaaa-bbbb-cccc-151515151515", "displayName": "Paola Castillo (Administración)", "mail": "paola.castillo@empresa.com.co", "jobTitle": "Asistente Administrativa", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=1800)).isoformat() + "Z", "lastSignInDaysAgo": 180, "activity_level": "baja", "storage_usage": "critical", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "16161616-aaaa-bbbb-cccc-161616161616", "displayName": "Ricardo Solano (Contratista)", "mail": "ricardo.solano@empresa.com.co", "jobTitle": "Contratista", "officeLocation": "Externo", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=60)).isoformat() + "Z", "lastSignInDaysAgo": 7, "activity_level": "media", "storage_usage": "low", "assignedLicenses": [{"skuId": "f30db892-07e9-47e9-837c-80727f46fd3d"}]},
    {"id": "17171717-aaaa-bbbb-cccc-171717171717", "displayName": "Sandra Méndez (Cuenta Inactiva)", "mail": "sandra.mendez@empresa.com.co", "jobTitle": "Ex-empleada", "officeLocation": "N/A", "accountEnabled": False, "createdDateTime": (SIMULATION_TODAY - timedelta(days=2000)).isoformat() + "Z", "lastSignInDaysAgo": 400, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "18181818-aaaa-bbbb-cccc-181818181818", "displayName": "Tomás Arango (Director)", "mail": "tomas.arango@empresa.com.co", "jobTitle": "Director Financiero", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=3000)).isoformat() + "Z", "lastSignInDaysAgo": 4, "activity_level": "media", "storage_usage": "medium", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}]},
    {"id": "19191919-aaaa-bbbb-cccc-191919191919", "displayName": "Úrsula Valdés (Comunicaciones)", "mail": "ursula.valdes@empresa.com.co", "jobTitle": "Comunicadora Social", "officeLocation": "Medellín", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=150)).isoformat() + "Z", "lastSignInDaysAgo": 10, "activity_level": "alta", "storage_usage": "low", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}, {"skuId": "1f2f344a-700d-42c9-9427-5cea1d5d7ba6"}]},
    {"id": "20202020-aaaa-bbbb-cccc-202020202020", "displayName": "Víctor Zabala (Sin Licencia)", "mail": "victor.zabala@empresa.com.co", "jobTitle": "Auxiliar de Bodega", "officeLocation": "Barranquilla", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=50)).isoformat() + "Z", "lastSignInDaysAgo": 32, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": []},
    {"id": "21212121-aaaa-bbbb-cccc-212121212121", "displayName": "Walter White (Químico)", "mail": "walter.white@empresa.com.co", "jobTitle": "Profesor de Química", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=450)).isoformat() + "Z", "lastSignInDaysAgo": 3, "activity_level": "alta", "storage_usage": "medium", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}]},
    {"id": "22222223-aaaa-bbbb-cccc-222222222223", "displayName": "Ximena Roldán (Auditoría)", "mail": "ximena.roldan@empresa.com.co", "jobTitle": "Auditora Interna", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=220)).isoformat() + "Z", "lastSignInDaysAgo": 12, "activity_level": "media", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}, {"skuId": "f30db892-07e9-47e9-837c-80727f46fd3d"}]},
    {"id": "23232323-aaaa-bbbb-cccc-232323232323", "displayName": "Yara Montes (Servicio al Cliente)", "mail": "yara.montes@empresa.com.co", "jobTitle": "Agente de Servicio", "officeLocation": "Cali", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=60)).isoformat() + "Z", "lastSignInDaysAgo": 28, "activity_level": "media", "storage_usage": "high", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "24242424-aaaa-bbbb-cccc-242424242424", "displayName": "Zoe Castro (Sin Licencia - Inactiva)", "mail": "zoe.castro@empresa.com.co", "jobTitle": "Ex-pasante", "officeLocation": "N/A", "accountEnabled": False, "createdDateTime": (SIMULATION_TODAY - timedelta(days=380)).isoformat() + "Z", "lastSignInDaysAgo": 200, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": []},
    
    # ### MODIFICADO: Usuario configurado para garantizar 'Sin Actividad' ###
    {"id": "25252525-aaaa-bbbb-cccc-252525252525", "displayName": "Andrés Buitrago (Sin Actividad)", "mail": "andres.buitrago@empresa.com.co", "jobTitle": "Analista de Datos Jr", "officeLocation": "Medellín", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=150)).isoformat() + "Z", "lastSignInDaysAgo": 75, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}]},

    {"id": "26262626-aaaa-bbbb-cccc-262626262626", "displayName": "Brenda Cárdenas (3-6 meses)", "mail": "brenda.cardenas@empresa.com.co", "jobTitle": "Tesorera", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=1000)).isoformat() + "Z", "lastSignInDaysAgo": 150, "activity_level": "baja", "storage_usage": "critical", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    
    # ### MODIFICADO: Usuario configurado para garantizar 'Sin Actividad' ###
    {"id": "27272727-aaaa-bbbb-cccc-272727272727", "displayName": "Camilo Díaz (Sin Actividad)", "mail": "camilo.diaz@empresa.com.co", "jobTitle": "Gerente Regional", "officeLocation": "Barranquilla", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=2000)).isoformat() + "Z", "lastSignInDaysAgo": 300, "activity_level": "ninguna", "storage_usage": "medium", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}]},
    
    {"id": "28282828-aaaa-bbbb-cccc-282828282828", "displayName": "Diana Fuentes (Más de 1 año)", "mail": "diana.fuentes@empresa.com.co", "jobTitle": "Asesora Legal", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=1300)).isoformat() + "Z", "lastSignInDaysAgo": 400, "activity_level": "baja", "storage_usage": "high", "assignedLicenses": [{"skuId": "46c3a859-c90d-40b3-9551-6178a48d5c18"}]},
    {"id": "29292929-aaaa-bbbb-cccc-292929292929", "displayName": "Esteban Guerrero (Más de 2 años)", "mail": "esteban.guerrero@empresa.com.co", "jobTitle": "Arquitecto de Soluciones", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=3000)).isoformat() + "Z", "lastSignInDaysAgo": 800, "activity_level": "baja", "storage_usage": "medium", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}]},
    {"id": "30303030-aaaa-bbbb-cccc-303030303030", "displayName": "Fabiana Hoyos (Nunca ha iniciado)", "mail": "fabiana.hoyos@empresa.com.co", "jobTitle": "Analista de Mercadeo", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=40)).isoformat() + "Z", "lastSignInDaysAgo": None, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "31313131-aaaa-bbbb-cccc-313131313131", "displayName": "Gerardo Luna (Bloqueado)", "mail": "gerardo.luna@empresa.com.co", "jobTitle": "Ex-Coordinador", "officeLocation": "N/A", "accountEnabled": False, "createdDateTime": (SIMULATION_TODAY - timedelta(days=600)).isoformat() + "Z", "lastSignInDaysAgo": 250, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "32323232-aaaa-bbbb-cccc-323232323232", "displayName": "Hilda Parra (Actividad Reciente)", "mail": "hilda.parra@empresa.com.co", "jobTitle": "Secretaria Ejecutiva", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=2500)).isoformat() + "Z", "lastSignInDaysAgo": 2, "activity_level": "alta", "storage_usage": "high", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}]},
    {"id": "33333334-aaaa-bbbb-cccc-333333333334", "displayName": "Iván Quiroga (Sin Licencia)", "mail": "ivan.quiroga@empresa.com.co", "jobTitle": "Mensajero", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=80)).isoformat() + "Z", "lastSignInDaysAgo": 20, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": []},
    {"id": "34343434-aaaa-bbbb-cccc-343434343434", "displayName": "Jimena Vélez (Licencia Gratuita)", "mail": "jimena.velez@empresa.com.co", "jobTitle": "Pasante Universitaria", "officeLocation": "Medellín", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=100)).isoformat() + "Z", "lastSignInDaysAgo": 18, "activity_level": "media", "storage_usage": "medium", "assignedLicenses": [{"skuId": "f30db892-07e9-47e9-837c-80727f46fd3d"}]},
    {"id": "35353535-aaaa-bbbb-cccc-353535353535", "displayName": "Kevin Acuña (Inactivo + de 1 año)", "mail": "kevin.acuna@empresa.com.co", "jobTitle": "Ex-analista", "officeLocation": "N/A", "accountEnabled": False, "createdDateTime": (SIMULATION_TODAY - timedelta(days=900)).isoformat() + "Z", "lastSignInDaysAgo": 500, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "36363636-aaaa-bbbb-cccc-363636363636", "displayName": "Lorena Mesa (IT Junior)", "mail": "lorena.mesa@empresa.com.co", "jobTitle": "Desarrolladora Junior", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=180)).isoformat() + "Z", "lastSignInDaysAgo": 4, "activity_level": "muy_alta", "storage_usage": "high", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}, {"skuId": "dcb1a3ae-b33f-4487-846a-a640262fadf4"}]},
    {"id": "37373737-aaaa-bbbb-cccc-373737373737", "displayName": "Manuel Noreña (Entre 7 y 15 días)", "mail": "manuel.norena@empresa.com.co", "jobTitle": "Supervisor de Planta", "officeLocation": "Cali", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=1400)).isoformat() + "Z", "lastSignInDaysAgo": 14, "activity_level": "media", "storage_usage": "medium", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
    {"id": "38383838-aaaa-bbbb-cccc-383838383838", "displayName": "Nidia Ocampo (Sin Licencia Activa)", "mail": "nidia.ocampo@empresa.com.co", "jobTitle": "Recepcionista", "officeLocation": "Bogotá", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=320)).isoformat() + "Z", "lastSignInDaysAgo": 22, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": []},
    {"id": "39393939-aaaa-bbbb-cccc-393939393939", "displayName": "Omar Prieto (Visio)", "mail": "omar.prieto@empresa.com.co", "jobTitle": "Arquitecto de Procesos", "officeLocation": "Remoto", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=480)).isoformat() + "Z", "lastSignInDaysAgo": 9, "activity_level": "alta", "storage_usage": "critical", "assignedLicenses": [{"skuId": "6fd2c87f-b296-42f0-b197-1e91e994b900"}, {"skuId": "4b244418-9658-4451-a2b8-b5e2b364e9bd"}]},
    {"id": "40404040-aaaa-bbbb-cccc-404040404040", "displayName": "Patricia Quintero (Nunca ha iniciado)", "mail": "patricia.quintero@empresa.com.co", "jobTitle": "Auxiliar Contable", "officeLocation": "Cali", "accountEnabled": True, "createdDateTime": (SIMULATION_TODAY - timedelta(days=15)).isoformat() + "Z", "lastSignInDaysAgo": None, "activity_level": "ninguna", "storage_usage": "low", "assignedLicenses": [{"skuId": "4b585984-651b-448a-9e53-3b10f069cf7f"}]},
]

# ==============================================================================
#  🏢 PERFILES DE SITIOS DE SHAREPOINT (40 Sitios para mayor cobertura de filtros)
# ==============================================================================
SITE_PROFILES = [
    # Escenario VERDE (uso bajo)
    {"displayName": "Intranet Corporativa", "lastActivityDaysAgo": 2, "fileCount": 1250, "activeFileCount": 300, "pageViewCount": 2500, "storageUsed_gb": 150, "storageAllocated_gb": 25600},
    {"displayName": "Recursos Humanos", "lastActivityDaysAgo": 5, "fileCount": 800, "activeFileCount": 150, "pageViewCount": 1200, "storageUsed_gb": 80, "storageAllocated_gb": 1024},
    # Escenario AMARILLO (uso medio/advertencia, ~75%-90%)
    {"displayName": "Gestión de Proyectos", "lastActivityDaysAgo": 1, "fileCount": 3400, "activeFileCount": 900, "pageViewCount": 800, "storageUsed_gb": 380, "storageAllocated_gb": 500},
    {"displayName": "Finanzas y Contabilidad", "lastActivityDaysAgo": 3, "fileCount": 2100, "activeFileCount": 400, "pageViewCount": 600, "storageUsed_gb": 850, "storageAllocated_gb": 1024},
    # Escenario ROJO (uso alto/crítico, >90%)
    {"displayName": "Marketing Digital", "lastActivityDaysAgo": 1, "fileCount": 5500, "activeFileCount": 1200, "pageViewCount": 3500, "storageUsed_gb": 720, "storageAllocated_gb": 750},
    {"displayName": "Archivo Legal (Inactivo)", "lastActivityDaysAgo": 400, "fileCount": 9500, "activeFileCount": 10, "pageViewCount": 50, "storageUsed_gb": 1180, "storageAllocated_gb": 1200},
    # --- Resto de los sitios con valores variados ---
    {"displayName": "Ventas Nacionales", "lastActivityDaysAgo": 7, "fileCount": 1800, "activeFileCount": 250, "pageViewCount": 950, "storageUsed_gb": 180, "storageAllocated_gb": 25600},
    {"displayName": "Soporte TI", "lastActivityDaysAgo": 0, "fileCount": 600, "activeFileCount": 200, "pageViewCount": 1800, "storageUsed_gb": 50, "storageAllocated_gb": 1024},
    {"displayName": "Innovación y Desarrollo", "lastActivityDaysAgo": 4, "fileCount": 850, "activeFileCount": 350, "pageViewCount": 400, "storageUsed_gb": 120, "storageAllocated_gb": 512},
    {"displayName": "Capacitaciones", "lastActivityDaysAgo": 25, "fileCount": 450, "activeFileCount": 50, "pageViewCount": 2200, "storageUsed_gb": 200, "storageAllocated_gb": 1024},
    {"displayName": "Comité de Dirección", "lastActivityDaysAgo": 10, "fileCount": 150, "activeFileCount": 80, "pageViewCount": 300, "storageUsed_gb": 30, "storageAllocated_gb": 256},
    {"displayName": "Calidad y Procesos", "lastActivityDaysAgo": 18, "fileCount": 1300, "activeFileCount": 100, "pageViewCount": 700, "storageUsed_gb": 160, "storageAllocated_gb": 25600},
    {"displayName": "Evento Anual 2024 (Archivado)", "lastActivityDaysAgo": 250, "fileCount": 2000, "activeFileCount": 5, "pageViewCount": 150, "storageUsed_gb": 350, "storageAllocated_gb": 512},
    {"displayName": "Logística y Bodega", "lastActivityDaysAgo": 12, "fileCount": 300, "activeFileCount": 40, "pageViewCount": 100, "storageUsed_gb": 40, "storageAllocated_gb": 25600},
    {"displayName": "Comunicaciones Internas", "lastActivityDaysAgo": 2, "fileCount": 900, "activeFileCount": 280, "pageViewCount": 2800, "storageUsed_gb": 90, "storageAllocated_gb": 1024},
    {"displayName": "Seguridad de la Información", "lastActivityDaysAgo": 30, "fileCount": 250, "activeFileCount": 30, "pageViewCount": 450, "storageUsed_gb": 60, "storageAllocated_gb": 25600},
    {"displayName": "Diseño UX-UI", "lastActivityDaysAgo": 6, "fileCount": 1600, "activeFileCount": 500, "pageViewCount": 650, "storageUsed_gb": 280, "storageAllocated_gb": 400},
    {"displayName": "Alianzas Estratégicas", "lastActivityDaysAgo": 50, "fileCount": 200, "activeFileCount": 20, "pageViewCount": 200, "storageUsed_gb": 25, "storageAllocated_gb": 25600},
    {"displayName": "Sitio de Pruebas (temporal)", "lastActivityDaysAgo": 95, "fileCount": 50, "activeFileCount": 2, "pageViewCount": 30, "storageUsed_gb": 5, "storageAllocated_gb": 100},
    {"displayName": "Gestión Documental", "lastActivityDaysAgo": 3, "fileCount": 15000, "activeFileCount": 1500, "pageViewCount": 1100, "storageUsed_gb": 2200, "storageAllocated_gb": 5120},
    {"displayName": "Onboarding Nuevos Empleados", "lastActivityDaysAgo": 8, "fileCount": 120, "activeFileCount": 80, "pageViewCount": 1500, "storageUsed_gb": 15, "storageAllocated_gb": 25600},
    {"displayName": "Planeación Estratégica 2025", "lastActivityDaysAgo": 22, "fileCount": 75, "activeFileCount": 60, "pageViewCount": 450, "storageUsed_gb": 20, "storageAllocated_gb": 1024},
    {"displayName": "Políticas y Procedimientos", "lastActivityDaysAgo": 100, "fileCount": 300, "activeFileCount": 15, "pageViewCount": 3000, "storageUsed_gb": 50, "storageAllocated_gb": 25600},
    {"displayName": "Archivo de Proyectos 2023", "lastActivityDaysAgo": 450, "fileCount": 4500, "activeFileCount": 1, "pageViewCount": 45, "storageUsed_gb": 850, "storageAllocated_gb": 900},
    {"displayName": "Ventas Internacionales", "lastActivityDaysAgo": 14, "fileCount": 950, "activeFileCount": 150, "pageViewCount": 8, "storageUsed_gb": 95, "storageAllocated_gb": 25600},
    {"displayName": "Blog Corporativo", "lastActivityDaysAgo": 5, "fileCount": 50, "activeFileCount": 25, "pageViewCount": 5500, "storageUsed_gb": 10, "storageAllocated_gb": 25600},
    {"displayName": "Sitio de Bienestar", "lastActivityDaysAgo": 28, "fileCount": 80, "activeFileCount": 10, "pageViewCount": 1800, "storageUsed_gb": 12, "storageAllocated_gb": 25600},
    {"displayName": "Tesorería", "lastActivityDaysAgo": 4, "fileCount": 1800, "activeFileCount": 300, "pageViewCount": 250, "storageUsed_gb": 320, "storageAllocated_gb": 1024},
    {"displayName": "Manual de Marca", "lastActivityDaysAgo": 200, "fileCount": 35, "activeFileCount": 5, "pageViewCount": 900, "storageUsed_gb": 8, "storageAllocated_gb": 50},
    {"displayName": "Auditoría Interna", "lastActivityDaysAgo": 40, "fileCount": 500, "activeFileCount": 50, "pageViewCount": 180, "storageUsed_gb": 70, "storageAllocated_gb": 25600},
    {"displayName": "Sitio Sin Visitas", "lastActivityDaysAgo": 60, "fileCount": 150, "activeFileCount": 20, "pageViewCount": 0, "storageUsed_gb": 18, "storageAllocated_gb": 25600},
    {"displayName": "Sitio Pocas Visitas", "lastActivityDaysAgo": 15, "fileCount": 200, "activeFileCount": 50, "pageViewCount": 9, "storageUsed_gb": 22, "storageAllocated_gb": 25600},
    {"displayName": "Sitio Visitas Moderadas", "lastActivityDaysAgo": 35, "fileCount": 400, "activeFileCount": 80, "pageViewCount": 48, "storageUsed_gb": 45, "storageAllocated_gb": 25600},
    {"displayName": "Sitio Sin Archivos Activos", "lastActivityDaysAgo": 80, "fileCount": 600, "activeFileCount": 0, "pageViewCount": 300, "storageUsed_gb": 60, "storageAllocated_gb": 25600},
    {"displayName": "Sitio Muy Inactivo (>1 año)", "lastActivityDaysAgo": 500, "fileCount": 1200, "activeFileCount": 2, "pageViewCount": 120, "storageUsed_gb": 150, "storageAllocated_gb": 25600},
    {"displayName": "Sitio Actividad 3-6 meses", "lastActivityDaysAgo": 120, "fileCount": 300, "activeFileCount": 30, "pageViewCount": 500, "storageUsed_gb": 35, "storageAllocated_gb": 25600},
    {"displayName": "Sitio Actividad 6-12 meses", "lastActivityDaysAgo": 280, "fileCount": 700, "activeFileCount": 15, "pageViewCount": 600, "storageUsed_gb": 80, "storageAllocated_gb": 25600},
    {"displayName": "Lanzamiento Producto X", "lastActivityDaysAgo": 9, "fileCount": 250, "activeFileCount": 180, "pageViewCount": 1100, "storageUsed_gb": 55, "storageAllocated_gb": 100},
    {"displayName": "Repositorio Legal", "lastActivityDaysAgo": 1, "fileCount": 8000, "activeFileCount": 100, "pageViewCount": 5, "storageUsed_gb": 1450, "storageAllocated_gb": 2048},
    {"displayName": "Sitio Completamente Inactivo", "lastActivityDaysAgo": 800, "fileCount": 100, "activeFileCount": 0, "pageViewCount": 0, "storageUsed_gb": 10, "storageAllocated_gb": 25600},
]

# ==============================================================================
# 🛠️ FUNCIONES GENERADORAS DE DATOS
# ==============================================================================
def get_activity_level_multiplier(level):
    return {"muy_alta": 2.5, "alta": 1.5, "media": 1, "baja": 0.3, "ninguna": 0}.get(level, 0)

def generate_dynamic_report_data(profiles, dias):
    report_data = []
    dias = int(dias)

    for user in profiles:
        multiplier = get_activity_level_multiplier(user["activity_level"])
        storage_tier = user.get("storage_usage", "low")

        # --- MODIFICACIÓN CLAVE ---
        # Ahora, si un usuario tiene "ninguna" actividad, su almacenamiento
        # también será CERO, además de sus otras métricas de actividad.
        
        outlook_used_bytes = 0
        onedrive_used_bytes = 0
        outlook_quota_bytes = 100 * (1024**3) # 100 GB
        onedrive_quota_bytes = 1 * (1024**4) # 1 TB

        if user["activity_level"] != "ninguna":
            # Para todos los demás usuarios, se calcula el almacenamiento como antes.
            if storage_tier == "critical":
                outlook_usage_ratio = random.uniform(0.95, 0.99)
                onedrive_usage_ratio = random.uniform(0.95, 0.99)
            elif storage_tier == "high":
                outlook_usage_ratio = random.uniform(0.75, 0.94)
                onedrive_usage_ratio = random.uniform(0.70, 0.94)
            elif storage_tier == "medium":
                outlook_usage_ratio = random.uniform(0.40, 0.74)
                onedrive_usage_ratio = random.uniform(0.30, 0.69)
            else: # low
                outlook_usage_ratio = random.uniform(0.05, 0.39)
                onedrive_usage_ratio = random.uniform(0.02, 0.29)
            
            outlook_used_bytes = int(outlook_quota_bytes * outlook_usage_ratio)
            onedrive_used_bytes = int(onedrive_quota_bytes * onedrive_usage_ratio)
        
        # --- Fin de la Lógica de Almacenamiento ---

        if user["lastSignInDaysAgo"] is not None:
            last_activity_date_str = (SIMULATION_TODAY - timedelta(days=user["lastSignInDaysAgo"])).strftime("%Y-%m-%d")
        else:
            last_activity_date_str = "Nunca"

        report_data.append({
            # Datos comunes
            "User Principal Name": user["mail"],
            "Display Name": user["displayName"],
            "Last Activity Date": last_activity_date_str,
            "Report Refresh Date": SIMULATION_TODAY.strftime("%Y-%m-%d"),
            # Outlook (será 0 si multiplier es 0)
            "Receive Count": str(int(random.randint(10, 50) * multiplier * (dias / 7))),
            "Send Count": str(int(random.randint(5, 25) * multiplier * (dias / 7))),
            "Item Count": str(int(5000 * multiplier) + random.randint(100, 5000)),
            "Storage Used (Byte)": str(outlook_used_bytes), # Ahora será 0 para inactivos
            "Prohibit Send Quota (Byte)": str(outlook_quota_bytes),
            "Has Archive": "False",
            # OneDrive (será 0 si multiplier es 0)
            "Viewed Or Edited File Count": str(int(random.randint(5, 30) * multiplier * (dias / 7))),
            "Synced File Count": str(int(random.randint(20, 100) * multiplier)),
            "File Count": str(int(800 * multiplier) + random.randint(50, 1000)),
            "Active File Count": str(int(150 * multiplier)),
            "Storage Used (Byte) OD": str(onedrive_used_bytes), # Ahora será 0 para inactivos
            "Storage Allocated (Byte) OD": str(onedrive_quota_bytes),
            # Teams (será 0 si multiplier es 0)
            "Private Chat Message Count": str(int(random.randint(20, 100) * multiplier * (dias / 7))),
            "Call Count": str(int(random.randint(2, 10) * multiplier * (dias / 7))),
            "Meeting Count": str(int(random.randint(3, 15) * multiplier * (dias / 7))),
            "Audio Duration In Seconds": str(int(random.randint(600, 3600) * multiplier * (dias / 30))),
            "Video Duration In Seconds": str(int(random.randint(300, 1800) * multiplier * (dias / 30))),
            "Screen Share Duration In Seconds": str(int(random.randint(400, 2200) * multiplier * (dias / 30))),
            # SharePoint (Actividad de Usuario)
            "Viewed Or Edited File Count SP": str(int(random.randint(5, 40) * multiplier * (dias / 7))),
            "Synced File Count SP": str(int(random.randint(2, 20) * multiplier)),
            "Visited Page Count SP": str(int(random.randint(10, 50) * multiplier * (dias / 7))),
        })
    return report_data

# ==============================================================================
# 🚀 OBJETOS FINALES EXPUESTOS POR EL MÓDULO
# ==============================================================================
usuarios_miembros_object = {"value": [{k: v for k, v in user.items() if k not in ["activity_level", "lastSignInDaysAgo", "storage_usage"]} for user in USER_PROFILES]}
usuarios_actividad_object = {"value": [{"id": user["id"], "signInActivity": {"lastSignInDateTime": (SIMULATION_TODAY - timedelta(days=user["lastSignInDaysAgo"])).isoformat() + "Z" if user["lastSignInDaysAgo"] is not None else None}} for user in USER_PROFILES]}

# Genera IDs únicos para cada sitio y los almacena para ser reutilizados
for site in SITE_PROFILES:
    site["full_id"] = f"empresa.sharepoint.com,{uuid.uuid4()},{uuid.uuid4()}"
    site["siteId_short"] = site["full_id"].split(',')[1]

sitios_sharepoint_object = {"value": [{"createdDateTime": (SIMULATION_TODAY - timedelta(days=random.randint(300,2000))).isoformat()+"Z", "id": site["full_id"], "webUrl": f"https://empresa.sharepoint.com/sites/{site['displayName'].replace(' ', '')}", "displayName": site["displayName"]} for site in SITE_PROFILES]}

def get_informe_sharepoint_uso_sitios(dias):
    data = []
    dias = int(dias)
    for site in SITE_PROFILES:
        actividad_en_periodo = site["lastActivityDaysAgo"] <= dias
        
        storage_allocated_bytes = int(site.get("storageAllocated_gb", 25600) * (1024**3))
        
        data.append({
            "Report Refresh Date": SIMULATION_TODAY.strftime("%Y-%m-%d"),
            "Site Id": site["siteId_short"],
            "Last Activity Date": (SIMULATION_TODAY - timedelta(days=site["lastActivityDaysAgo"])).strftime("%Y-%m-%d"),
            "File Count": str(site["fileCount"]),
            "Active File Count": str(site["activeFileCount"]) if actividad_en_periodo else "0",
            "Page View Count": str(site["pageViewCount"]) if actividad_en_periodo else "0",
            "Storage Used (Byte)": str(int(site["storageUsed_gb"] * (1024**3))),
            "Storage Allocated (Byte)": str(storage_allocated_bytes),
        })
    return data