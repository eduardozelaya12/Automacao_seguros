import pyautogui
import time
import json


# Configurações de segurança
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.8

def processar_automoveis():
    """
    Processa cadastro de automóveis a partir do JSON
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
    
    # ============================================
    # CARREGAR JSON
    # ============================================
    try:
        with open('carros.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Extrair dados de cada carro
        carros_ativos = []
        for item in dados:
            if 'output' in item:
                carros_ativos.append(item['output'])
        
        print(f"✅ JSON carregado: {len(carros_ativos)} automóvel(is)\n")
        
    except Exception as e:
        print(f"❌ Erro ao carregar JSON: {e}")
        return
    
    # ============================================
    # LOGIN E NAVEGAÇÃO (assumindo que já está na tela correta)
    # ============================================
    print("⏳ Aguarde 3 segundos para posicionar na janela...\n")
    time.sleep(3)
    
    # ============================================
    # PROCESSAR CADA AUTOMÓVEL
    # ============================================
    for i, carro in enumerate(carros_ativos, 1):

        # Navegar com TAB até o local desejado  
        pyautogui.press('enter')
        time.sleep(5)
        for _ in range(5):
            pyautogui.press('tab')
        print(f"   ✅ Botão encontrado - clicando...")
        pyautogui.press('enter')

        # AJUSTE PARA DEFINIR A COMPANIA DO SEGURO
        pyautogui.press('s')
        pyautogui.press('tab')
        # AJUSTE PARA DEFINIR O RAMO: AUTOMOVIL,ETC
        for _ in range(4):
            pyautogui.press('down')
        # CONFIRMAR    
        pyautogui.press('tab')
        pyautogui.press('enter')   

        # Extrair seções do JSON
        poliza = carro.get('datos_poliza', {})
        basicos = carro.get('datos_basicos', {})
        vehiculo = carro.get('datos_vehiculo', {})
        cobertura = carro.get('datos_cobertura', {})
        pago = carro.get('condiciones_pago', {})
        cliente = carro.get('datos_cliente', {})
        
        print(f"\n{'='*60}")
        print(f"[{i}/{len(carros_ativos)}] 🚗 {vehiculo.get('marca_modelo', 'N/A')}")
        print(f"{'='*60}\n")
        
        time.sleep(5)
        pyautogui.press('enter')
        # DATOS DE LA POLIZA
        # 13 tabs me leva para o Desde de Datos de la Poliza
        for _ in range(13):
            pyautogui.press('tab')

        pyautogui.write(poliza.get('numero_poliza', 'N/A')) # Numero de la poliza ajustado

        # DATOS DEL VEHICULO
        # 2 tabs me leva para inserir o valor de la Marca e Modelo do Automovil
        pyautogui.press('tab') 
        pyautogui.press('tab')
        pyautogui.write(vehiculo.get('marca_modelo', 'N/A')) # Valor da Marca e Modelo do Automovil

        # 1 tab para inserir o valor do Ano do Automovil
        pyautogui.press('tab')
        pyautogui.write(vehiculo.get('ano', 'N/A')) # Valor do Ano do Automovil

        # 2 tab para inserir o valor de combustivel do Automovil
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write(vehiculo.get('combustible', 'N/A')) # Valor do Ano do Automovil

        pyautogui.press('tab')
        pyautogui.press('tab')
        # 1 tab para inserir o valor de categoria do vehiculo
        categoria = vehiculo.get('categoria', 'N/A')
        
        # Mapeamento de todas as categorias de veículos (baseado na ordem do dropdown)
        # O valor representa o número de vezes que 'down' precisa ser pressionado
        # para selecionar a categoria, considerando que o primeiro item requer 1 'down'.
        categorias_map = {
            "AMBULANCIA": 1,
            "AUTOMOVIL": 2,
            "CABINA EXTENDIDA": 3,
            "CAMION": 4,
            "CAMIONETA": 5,
            "CASA RODANTE": 6,
            "CHATA": 7,
            "CISTERNA": 8,
            "CUADRICICLOS": 9,
            "DOBLE CABINA": 10,
            "EXCAVADORA": 11,
            "FURGON": 12,
            "JEEP": 13,
            "MAQ. AUTOMOTRIZ": 14,
            "MINI BUS": 15,
            "MOTO": 16,
            "MOTORHOME": 17,
            "OMNIBUS": 18,
            "PICK UP": 19,
            "REMOLQUE": 20,
            "RETROEXCAVADORA": 21,
            "RURAL": 22,
            "SEMIREMOLQUE": 23,
            "TRACTOR": 24,
            "TRAILER": 25
        }
        
        # Navegar até a categoria correta
        if categoria in categorias_map:
            for _ in range(categorias_map[categoria]):
                pyautogui.press('down')
            print(f"   ✅ Categoria selecionada: {categoria}")
        else:
            print(f"   ⚠️ Categoria desconhecida: {categoria}")
            
        # 1 tab para inserir o valor do motor do vehiculo
        pyautogui.press('tab')
        pyautogui.write(vehiculo.get('motor', 'N/A'))
        
        # 1 tab para inserir o valor do chasis do vehiculo
        pyautogui.press('tab')
        pyautogui.write(vehiculo.get('chasis', 'N/A'))
                    
        # 2 tabs para inseri valor de destino de uso / Dropdown
        pyautogui.press('tab')
        pyautogui.press('tab')
        destino = vehiculo.get('destino', 'N/A')
        
        # Mapeamento de todos os destinos de uso (baseado na ordem do dropdown)
        destinos_map = {
            "ALQUILER SIN CHOFER": 1,
            "AUXILIO MECANICO": 2,
            "COMERCIAL": 3,
            "EASY GO Y UBER": 4,
            "PARTICULAR": 5,
            "PARTICULAR Y TRABAJO": 6,
            "PASEO": 7,
            "PLACER": 8,
            "REMISE": 9,
            "TAXIMETROS": 10,
            "TRABAJO": 11,
            "TRABAJO PERSONAL": 12,
            "UBER": 13
        }
        
        # Navegar até o destino correto
        if destino in destinos_map:
            for _ in range(destinos_map[destino]):
                pyautogui.press('down')
            print(f"   ✅ Destino selecionado: {destino}")
        else:
            print(f"   ⚠️ Destino desconhecido: {destino}")

        # 1 tab para inserir o valor de calidad
        pyautogui.press('tab')
        calidad = vehiculo.get('calidad', 'N/A')
        
        # Mapeamento de calidad (baseado na ordem do dropdown)
        calidad_map = {
            "ARRENDATARIO": 1,
            "PR. COMPRADOR": 2,
            "PROPIETARIO": 3,
            "USUARIO": 4
        }
        
        # Navegar até a calidad correta
        if calidad in calidad_map:
            for _ in range(calidad_map[calidad]):
                pyautogui.press('down')
            print(f"   ✅ Calidad selecionada: {calidad}")
        else:
            print(f"   ⚠️ Calidad desconhecida: {calidad}") 

        # 5 tabs para inserir o valor de la cobertura
        for _ in range(5):
            pyautogui.press('tab')
        
        cobertura_tipo = cobertura.get('cobertura', 'N/A')
        
        # Mapeamento de tipos de cobertura (baseado na ordem do dropdown)
        cobertura_map = {
            "BASICA": 1,
            "TERCEROS": 2,
            "TERC.+ROBO+INCENDIO": 3,
            "TODO RIESGO": 4,
            "T=H+I [RC USD 200,000]": 5,
            "BASICA+ AUXILIO": 6,
            "RC- BASICA": 7,
            "RC- ESTANDAR": 8,
            "RC- PLUS": 9,
            "T=H+I/ C1": 10,
            "T=H+I/ C PLUS": 11,
            "T=H+I/ C MEGA": 12,
            "TODO RIESGO/ D1": 13,
            "TODO RIESGO/D4": 14,
            "TODO RIESGO/ D PLUS": 15
        }
        
        # Navegar até o tipo de cobertura correto
        if cobertura_tipo in cobertura_map:
            for _ in range(cobertura_map[cobertura_tipo]):
                pyautogui.press('down')
            print(f"   ✅ Cobertura selecionada: {cobertura_tipo}")
        else:
            print(f"   ⚠️ Cobertura desconhecida: {cobertura_tipo}")
    
        # tabs para inserir dado de zona de circulação
        for _ in range(4):
            pyautogui.press('tab')

        zona_circulacao = cobertura.get('zona_circulacao_corrigida', 'N/A')
        
        # Mapeamento de zonas de circulação (baseado na ordem do dropdown)
        zona_circulacao_map = {
            "AMBITO NACIONAL E INTERNACIONAL": 1,
            "ARGENTINA": 2,
            "ARTIGAS": 3,
            "CANELONES": 4,
            "CANELONES NORTE": 5,
            "CANELONES SUR": 6,
            "CERRO LARGO": 7,
            "CIUDAD DE LA COSTA": 8,
            "COLONIA": 9,
            "COSTA DE ORO": 10,
            "DURAZNO": 11,
            "FLORES": 12,
            "FLORIDA": 13,
            "MALILEA": 14,
            "MALDONADO": 15,
            "MONTEVIDEO": 16,
            "OTROS": 17,
            "PAYSANDU": 18,
            "RESTO DEL PAIS": 19,
            "RIO NEGRO": 20,
            "RIVERA": 21,
            "ROCHA": 22,
            "SALTO": 23,
            "SAN JOSE": 24,
            "SOLO AMBITO NACIONAL": 25,
            "SORIANO": 26,
            "TACUAREMBO": 27,
            "TREINTA Y TRES": 28
        }
        
        # Navegar até a zona de circulação correta
        if zona_circulacao in zona_circulacao_map:
            for _ in range(zona_circulacao_map[zona_circulacao]):
                pyautogui.press('down')
            print(f"   ✅ Zona de circulação selecionada: {zona_circulacao}")
        else:
            print(f"   ⚠️ Zona de circulação desconhecida: {zona_circulacao}")

        for _ in range(2):
            pyautogui.press('tab')
        pyautogui.write(str(cobertura.get('deducible', 'N/A')))

        # Inserir valor de moeda
        pyautogui.press('tab')
        # Aqui se digitar somente a primeira letra, o campo já completa automaticamente
        moneda = cobertura.get('moneda', 'N/A')
        print(moneda)
        if moneda == "PES":
                print("aquiii moneda"+str(_))
                pyautogui.write('P')
        elif moneda == "DOL":
            print("aquiii moneda"+str(_))
            pyautogui.write('D')

        for _ in range(2):
            pyautogui.press('tab')
        # Inserir valor de moeda em Moneda em Condiciones de Pago
        pago_moneda = pago.get('moneda', 'N/A')
        if pago_moneda == "PES":
            pyautogui.write('P')
        elif pago_moneda == "DOL":
            pyautogui.write('D')

        
        # Inserir valor de cuotas
        pyautogui.press('tab')
        pyautogui.write(str(pago.get('cuotas', 'N/A')))

        # Inserir valor total
        pyautogui.press('tab')
        pyautogui.write(str(pago.get('total', 'N/A')))

        # Inserir valor de Premio
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.write(str(pago.get('premio_total', 'N/A')))

        for _ in range(20):
            pyautogui.press('tab')

        nome_assegurado_raw = cliente.get('assegurado', 'N/A')
        if ',' in nome_assegurado_raw and nome_assegurado_raw != 'N/A':
            partes = [p.strip() for p in nome_assegurado_raw.split(',', 1)]
            nome_assegurado = f"{partes[1]} {partes[0]}"
        else:
            nome_assegurado = nome_assegurado_raw
        pyautogui.write(str(nome_assegurado))

        
        for _ in range(25):
            pyautogui.press('tab')
        # pyautogui.press('enter')
        for _ in range(2):
            pyautogui.press('enter')
    # ============================================
    # FIM
    # ============================================
    print(f"\n{'='*60}")
    print(f"✅ AUTOMAÇÃO CONCLUÍDA")
    # print(f"🚗 Total processado: {len(carros_ativos)} automóvel(is)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    try:
        processar_automoveis()
    except KeyboardInterrupt:
        print("\n\n⚠️  Automação interrompida pelo usuário (Ctrl+C)")
    except pyautogui.FailSafeException:
        print("\n\n⚠️  Automação interrompida (FAILSAFE - mouse no canto)")
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
