import flet as ft
import math

def main(page: ft.Page):
    # ページの設定
    page.title = "Flet Calculator"
    
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.window_resizable = False 
    page.window_width = 360 
    page.window_height = 700 
    page.bgcolor = ft.colors.BLACK 

    # --- 電卓の状態を保持する変数 ---
    current_input = "0"
    previous_input = ""
    operator = None 
    reset_display = False 
    
    # 科学計算用の角度モード (デフォルトは度数法)
    angle_mode = "deg" 

    # --- UI要素 ---
    # 結果表示ディスプレイ
    display = ft.Text(
        value=current_input,
        size=60, 
        color=ft.colors.WHITE,
        text_align=ft.TextAlign.RIGHT,
        max_lines=1, 
        overflow=ft.TextOverflow.FADE, 
    )

    # --- ボタンのクリックハンドラ関数 ---
    def button_click(e):
        # 必要な状態変数を nonlocal で参照
        nonlocal current_input, previous_input, operator, reset_display, angle_mode
        
        button_text = e.control.text
        button_action = e.control.data 

        # 数字ボタン (0-9) および '.' ボタンの処理
        if button_text.isdigit() or button_text == ".":
            # 小数点ボタンの処理
            if button_text == ".":
                if reset_display:
                    current_input = "0."
                    reset_display = False
                elif "." not in current_input: 
                    current_input += "."
            # 数字ボタンの処理
            else:
                if current_input == "0" or reset_display:
                    current_input = button_text
                    reset_display = False
                else:
                    current_input += button_text
        
        # AC (All Clear) ボタン
        elif button_text == "AC":
            current_input = "0"
            previous_input = ""
            operator = None
            reset_display = False
            
        # +/- (符号反転) ボタン
        elif button_text == "+/-":
            try: 
                current_input = str(float(current_input) * -1)
            except ValueError:
                current_input = "Error" 
        
        # % (パーセンテージ) ボタン
        elif button_text == "%":
            try:
                current_input = str(float(current_input) / 100)
            except ValueError:
                current_input = "Error"

        # 演算子 (+, -, ×, ÷) ボタン
        elif button_action in ["add", "subtract", "multiply", "divide"]:
            if previous_input and operator and not reset_display:
                current_input = calculate(previous_input, current_input, operator)
            operator = button_action 
            previous_input = current_input 
            reset_display = True 
            
        # = (計算実行) ボタン
        elif button_text == "=":
            if previous_input and operator: # 前回の数値と演算子があれば計算
                current_input = calculate(previous_input, current_input, operator)
                operator = None 
                previous_input = "" 
                reset_display = True 
        
        # 科学計算ボタンの処理 (フェーズ2で実装)
        elif button_action in ["sin", "cos", "tan", "sqrt", "log", "exp", "pi", "e_const", "rad-deg"]:
            handle_scientific_function(button_action)

        # ディスプレイの値を更新し、ページを再描画
        display.value = current_input
        page.update()

    # --- 実際の計算を行うヘルパー関数 ---
    def calculate(num1_str, num2_str, op):
        try:
            n1 = float(num1_str)
            n2 = float(num2_str)
        except ValueError:
            return "Error (Invalid input)" 

        if op == "add":
            return str(n1 + n2)
        elif op == "subtract":
            return str(n1 - n2)
        elif op == "multiply":
            return str(n1 * n2)
        elif op == "divide":
            if n2 == 0:
                return "Error (Div by 0)" 
            return str(n1 / n2)
        return num2_str 

    # --- ボタンコントロールを作成するヘルパー関数 ---
    def create_button(text, bgcolor, text_color, col_span=1, action=None):
       
        btn_style = ft.ButtonStyle(
            shape={
                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=35), 
            },
            bgcolor={
                ft.MaterialState.DEFAULT: bgcolor,
                ft.MaterialState.HOVERED: ft.colors.with_opacity(0.8, bgcolor), 
            },
            color={
                ft.MaterialState.DEFAULT: text_color,
            },
            padding=0, 
        )

        return ft.Container(
            content=ft.ElevatedButton(
                text=text,
                on_click=button_click,
                style=btn_style,
                data=action if action else text, 
            ),
            width=70 if col_span == 1 else (70 * col_span + (col_span - 1) * 10), 
            height=70,
            alignment=ft.alignment.center,
            col_span=col_span,
        )

    # --- 科学計算関数ハンドラ (フェーズ2で詳細を実装) ---
    def handle_scientific_function(action):
        nonlocal current_input, reset_display, angle_mode
        try:
            value = float(current_input)
        except ValueError:
            current_input = "Error"
            page.update()
            return

        result = None
        
        if action == "sin":
            rad_value = value * (math.pi / 180) if angle_mode == "deg" else value
            result = math.sin(rad_value)
        elif action == "cos":
            rad_value = value * (math.pi / 180) if angle_mode == "deg" else value
            result = math.cos(rad_value)
        elif action == "tan":
            rad_value = value * (math.pi / 180) if angle_mode == "deg" else value
            
            if angle_mode == "deg" and (value % 90 == 0 and value % 180 != 0):
                result = "Undefined"
            else:
                result = math.tan(rad_value)
        elif action == "sqrt": 
            if value < 0:
                result = "Error (Imaginary)" 
            else:
                result = math.sqrt(value)
        elif action == "log": 
            if value <= 0:
                result = "Error (Non-positive)"
            else:
                result = math.log(value) 
        elif action == "exp": 
            result = math.exp(value)
        elif action == "pi": 
            result = math.pi
            reset_display = False 
            
        elif action == "e_const": 
            result = math.e
            reset_display = False 
        elif action == "rad-deg":
            angle_mode = "rad" if angle_mode == "deg" else "deg"
            for control_container in page.controls[0].controls[3].controls: 
                if isinstance(control_container.content, ft.ElevatedButton) and control_container.content.data == "rad-deg":
                    control_container.content.text = angle_mode.upper()
                    break
            current_input = current_input 

        if result is not None:
            if isinstance(result, str): 
                current_input = result
            else:
               
                current_input = str(result)
            reset_display = True 

    # --- UIのレイアウト ---
    page.add(
        ft.Column(
            [
                ft.Container(height=page.window_height * 0.1), 
                ft.Row( 
                    [display],
                    alignment=ft.MainAxisAlignment.END, # 右寄せ
                    expand=True, 
                ),
                ft.Container(height=20),
                ft.GridView( 
                    runs_count=5, 
                    spacing=10, 
                    run_spacing=10, 
                    expand=True, 
                    padding=ft.padding.only(left=20, right=20, bottom=20), 
                    controls=[
                        # --- 1行目 ---
                        create_button("AC", ft.colors.GREY_700, ft.colors.BLACK, action="clear"),
                        create_button("+/-", ft.colors.GREY_700, ft.colors.BLACK, action="plus-minus"),
                        create_button("%", ft.colors.GREY_700, ft.colors.BLACK, action="percent"),
                        create_button("÷", ft.colors.ORANGE_600, ft.colors.WHITE, action="divide"),
                        create_button("sin", "#333333", ft.colors.WHITE, action="sin"), # 科学計算ボタン1

                        # --- 2行目 ---
                        create_button("7", "#505050", ft.colors.WHITE),
                        create_button("8", "#505050", ft.colors.WHITE),
                        create_button("9", "#505050", ft.colors.WHITE),
                        create_button("×", ft.colors.ORANGE_600, ft.colors.WHITE, action="multiply"),
                        create_button("cos", "#333333", ft.colors.WHITE, action="cos"), # 科学計算ボタン2

                        # --- 3行目 ---
                        create_button("4", "#505050", ft.colors.WHITE),
                        create_button("5", "#505050", ft.colors.WHITE),
                        create_button("6", "#505050", ft.colors.WHITE),
                        create_button("-", ft.colors.ORANGE_600, ft.colors.WHITE, action="subtract"),
                        create_button("tan", "#333333", ft.colors.WHITE, action="tan"), # 科学計算ボタン3

                        # --- 4行目 ---
                        create_button("1", "#505050", ft.colors.WHITE),
                        create_button("2", "#505050", ft.colors.WHITE),
                        create_button("3", "#505050", ft.colors.WHITE),
                        create_button("+", ft.colors.ORANGE_600, ft.colors.WHITE, action="add"),
                        create_button("log", "#333333", ft.colors.WHITE, action="log"), # 科学計算ボタン4 (自然対数 ln)

                        # --- 5行目 ---
                        create_button("0", "#505050", ft.colors.WHITE, col_span=2), # 0ボタンは2列分
                        create_button(".", "#505050", ft.colors.WHITE),
                        create_button("=", ft.colors.ORANGE_600, ft.colors.WHITE, action="calculate"),
                        create_button("e^x", "#333333", ft.colors.WHITE, action="exp"), # 科学計算ボタン5 (指数関数)

                        # --- 追加の科学計算ボタン ---
                        create_button("√", "#333333", ft.colors.WHITE, action="sqrt"), # 平方根
                        create_button("π", "#333333", ft.colors.WHITE, action="pi"),   # 円周率
                        create_button("e", "#333333", ft.colors.WHITE, action="e_const"), # 自然対数の底
                        create_button(angle_mode.upper(), ft.colors.GREY_700, ft.colors.WHITE, action="rad-deg"), # RAD/DEG切り替え
                    ],
                ) 
            ], 
            expand=True, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        ) 
    ) 

    # アプリケーションの初期表示を更新
    page.update()

# Fletアプリケーションとして実行
ft.app(target=main)