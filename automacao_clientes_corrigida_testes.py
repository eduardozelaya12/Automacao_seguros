"""
AUTOMAÇÃO DE CADASTRO DE CLIENTES - Versão Corrigida
Processa clientes do arquivo clientes.json
"""
import pyautogui
import time
import json

# Configurações de segurança
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.8

def safe_write(value, interval=0.1):
    """
    Escrever valor no PyAutoGUI apenas se não for None ou 'none'
    """
    if value and str(value).lower() != 'none' and str(value).strip() != '':
        pyautogui.write(str(value), interval=interval)
        return True
    return False

def processar_clientes():
    """
    Processa cadastro de clientes a partir do JSON
    """

    print("🔵 Abrindo Aplicacao de Seguros (Velneo vClient)...")
    pyautogui.press('win')
    time.sleep(0.5)
    pyautogui.write('velneo vClient', interval=0.1)
    time.sleep(0.5)
    pyautogui.press('enter')
    
    print("⏳ Aguardando janela de conexão carregar...")
    time.sleep(3)
    
    # Navegar para senha (2 TABs)
    pyautogui.press('tab')
    pyautogui.press('tab')
    
    print("🔐 Preenchendo campo Senha...")
    pyautogui.write('1234', interval=0.05)
    
    print("🔵 Conectando...")
    pyautogui.press('enter')
    
    time.sleep(0.5)
    
    print("🔵 Selecionando Portal...")
    pyautogui.press('enter')
    time.sleep(2.5)
    
    # Fechar notificação
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(1)
    
    
    
    
    print("\n" + "="*60)
    print("🎯 AUTOMAÇÃO: Cadastro de Clientes")
    print("="*60 + "\n")
    
    # ============================================
    # CARREGAR JSON
    # ============================================
    try:
        with open('clientes_exemplo_multiplos.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Ajustar para nova estrutura: clientes_json[0]['output']['datos_cliente']
        clientes_ativos = []


        for item in dados:
            if 'output' in item and 'datos_cliente' in item['output']:
                clientes_ativos.append(item['output']['datos_cliente'])
        
        print(f"✅ JSON carregado: {len(clientes_ativos)} cliente(s)\n")
        
    except Exception as e:
        print(f"❌ Erro ao carregar JSON: {e}")
        return
    
    # ============================================  
    # LOGIN (assumindo que já está logado)
    # ============================================
    print("⏳ Aguarde 3 segundos para posicionar na janela...\n")
    time.sleep(3)
    
    # ============================================
    # PROCESSAR CADA CLIENTE
    # ============================================
    for i, cliente in enumerate(clientes_ativos, 1):

        # Navegar com TAB até o local desejado  
        pyautogui.press('enter')
        time.sleep(5)
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        print(f"   ✅ Botão encontrado - clicando...")
        pyautogui.press('enter')
        
        print(f"\n{'='*60}")
        print(f"[{i}/{len(clientes_ativos)}] 👤 {cliente.get('assegurado', 'N/A')}")
        print(f"{'='*60}\n")
        
        # ============================================
        # PREENCHER NÚMERO DO CLIENTE
        # ============================================
        print("   📝 Número do cliente: ", cliente.get('numero_cliente'))
        numero = cliente.get('numero_cliente', 'N/A')
        safe_write(str(numero))
        
        assegurado = cliente.get('assegurado', '')
        if assegurado:
            for _ in range(7):
                pyautogui.press('tab')
            print(f"   📝 Assegurado: {assegurado}")
            safe_write(assegurado)

        # Preencher valor de tipo
        pyautogui.press('tab') 
        tipo = cliente.get('tipo', 'N/A')  # Exemplo de valor, substituir pelo valor do JSON
        if tipo == "Empresa":
                pyautogui.press('down')
                # Preencher valor de corredor
                pyautogui.press('tab')
                # A principio harcoded para Paulo 
                pyautogui.write('P')
                pyautogui.press('enter')

                # Preencher valor de corredor
                pyautogui.press('tab')
                # A principio harcoded para Paulo 
                pyautogui.write('P')
                pyautogui.press('enter')
                for _ in range(2):
                    pyautogui.press('tab')
                
                if cliente.get('rut'):
                    pyautogui.write(cliente.get('rut'), interval=0.1)
                pyautogui.press('tab')
                if cliente.get('razao_social'):
                    pyautogui.write(cliente.get('razao_social'), interval=0.1)
                pyautogui.press('tab')
                if cliente.get('categoria'):
                        pyautogui.press('tab')
                        pyautogui.write(cliente.get('categoria'), interval=0.1)

        elif tipo == "Particular" or tipo == "Otro":
            
                for _ in range(2):
                    pyautogui.press('down')
            # Preencher valor de corredor
                pyautogui.press('tab')
                # A principio harcoded para Paulo 
                pyautogui.write('P')
                pyautogui.press('enter')
                for _ in range(2):
                    pyautogui.press('tab')
            
                # Preecher valor de Documento
                if cliente.get('documento'):
                    pyautogui.write(cliente.get('documento'), interval=0.1)
                pyautogui.press('tab')
                if cliente.get('categoria'):
                        pyautogui.write(cliente.get('categoria'), interval=0.1)

        elif tipo == "Particular/Empresa":
                for _ in range(3):
                    pyautogui.press('down')
            # Preencher valor de corredor
                pyautogui.press('tab')
                # A principio harcoded para Paulo 
                pyautogui.write('P')
                pyautogui.press('enter')
                for _ in range(2):
                    pyautogui.press('tab')
                if cliente.get('rut'):
                    pyautogui.write(cliente.get('rut'), interval=0.1)
                pyautogui.press('tab')
                if cliente.get('razao_social'):
                    pyautogui.write(cliente.get('razao_social'), interval=0.1)
                pyautogui.press('tab')
                if cliente.get('documento'):
                      pyautogui.write(cliente.get('documento'), interval=0.1)
                pyautogui.press('tab')
                if cliente.get('categoria'):
                        pyautogui.write(cliente.get('categoria'), interval=0.1)
        elif tipo == "Edificio":
                for _ in range(4):
                    pyautogui.press('down')
            # Preencher valor de corredor
                pyautogui.press('tab')
                # A principio harcoded para Paulo 
                pyautogui.write('P')
                pyautogui.press('enter')
                pyautogui.press('tab') * 2
                if cliente.get('padron'):
                    pyautogui.write(cliente.get('padron'), interval=0.1)
                pyautogui.press('tab')
                if cliente.get('categoria'):
                        pyautogui.write(cliente.get('categoria'), interval=0.1)
        elif tipo == "Prospecto" or tipo == "Copropiedad":
                pyautogui.press('down') * 5
            # Preencher valor de corredor
                pyautogui.press('tab')
                # A principio harcoded para Paulo 
                pyautogui.write('P')
                pyautogui.press('enter')
                pyautogui.press('tab') * 2
                if cliente.get('categoria'):
                        pyautogui.write(cliente.get('categoria'), interval=0.1)
     

        # Preencher valor de telefono
        pyautogui.press('tab')
        safe_write(cliente.get('telefono'), interval=0.1)

        # Preencher valor de celular
        pyautogui.press('tab')
        safe_write(cliente.get('celular'), interval=0.1)

        # Preencher valor de Fecha Nascimiento
        pyautogui.press('tab')
        safe_write(cliente.get('fecha_nacimiento'), interval=0.1)

        # Preencher valor de Domicilio
        for _ in range(3):
            pyautogui.press('tab')
        safe_write(cliente.get('domicilio'), interval=0.1)

        # Preencher valor de Departamento
        pyautogui.press('tab')
        safe_write(cliente.get('Departamento'), interval=0.1)

        # Preencher valor de Localidad
        pyautogui.press('tab')
        safe_write(cliente.get('Localidad'), interval=0.1)
        
        # Preencher Codigo Postal
        pyautogui.press('tab')
        safe_write(cliente.get('codigo_postal'), interval=0.1)

        # Preencher valor de Dir. Cobro
        pyautogui.press('tab')
        safe_write(cliente.get('dir_cobro'), interval=0.1)

        # Preencher valor de Departamento (cobro)
        pyautogui.press('tab')
        safe_write(cliente.get('Departamento'), interval=0.1)

        # Preencher valor de Localidad (cobro)
        pyautogui.press('tab')
        safe_write(cliente.get('Localidad'), interval=0.1)

        # Preencher Codigo Postal (cobro)
        pyautogui.press('tab')
        safe_write(cliente.get('codigo_postal'), interval=0.1)

        # Preencher Email e Observações conforme tipo
        if tipo == "Particular" or tipo == "Edificio" or tipo == "Otro" or tipo == "Prospecto" or tipo == "Copropiedad":
                # Preencher valor de Email
                for _ in range(2):
                    pyautogui.press('tab')
                safe_write(cliente.get('email'), interval=0.1)
                # Preencher valor em Observaciones
                for _ in range(7):
                    pyautogui.press('tab')
                safe_write(cliente.get('Observaciones'), interval=0.1)
        else:
                # Preencher valor de Email
                for _ in range(3):
                    pyautogui.press('tab')
                safe_write(cliente.get('email'), interval=0.1)
                # Preencher valor em Observaciones
                for _ in range(7):
                    pyautogui.press('tab')
                safe_write(cliente.get('Observaciones'), interval=0.1)
        
        # ============================================
        # GUARDAR CLIENTE
        # ============================================
        for _ in range(9):
            pyautogui.press('tab')
        
        print("   💾 Guardando cliente...")
        for _ in range(2):
            pyautogui.press('enter')
        time.sleep(0.5)
        
        print(f"\n   ✅ Cliente processado com sucesso!\n")
        time.sleep(2)
        
    print(f"\n{'='*60}")
    print(f"✅ AUTOMAÇÃO CONCLUÍDA")
    print(f"📊 Total processado: {len(clientes_ativos)} cliente(s)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    try:
        processar_clientes()
    except KeyboardInterrupt:
        print("\n\n⚠️  Automação interrompida pelo usuário (Ctrl+C)")
    except pyautogui.FailSafeException:
        print("\n\n⚠️  Automação interrompida (FAILSAFE - mouse no canto)")
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
