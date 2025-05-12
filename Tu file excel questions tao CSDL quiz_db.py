import pandas as pd
import sqlite3

# Tên file Excel và tên cơ sở dữ liệu
excel_file = 'questions.xlsx'  # Thay bằng tên file Excel của bạn
database_file = 'quiz.db'

# Tên các bảng trong Excel (nếu có nhiều sheet) hoặc tên sheet chứa dữ liệu
questions_sheet = 'Questions'  # Thay bằng tên sheet chứa câu hỏi
options_sheet = 'Options'      # Thay bằng tên sheet chứa đáp án

# Tên bảng trong cơ sở dữ liệu SQLite
questions_table = 'questions'
options_table = 'options'

try:
    # Kết nối đến cơ sở dữ liệu SQLite (nếu chưa có sẽ tự động tạo)
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # --- Đọc dữ liệu từ sheet 'Questions' và tạo bảng 'questions' ---
    try:
        df_questions = pd.read_excel(excel_file, sheet_name=questions_sheet)
        # Lấy tên các cột từ DataFrame để tạo câu lệnh SQL
        columns_questions = ', '.join(df_questions.columns)
        placeholders_questions = ', '.join(['?'] * len(df_questions.columns))
        create_table_questions_sql = f'''
            CREATE TABLE IF NOT EXISTS {questions_table} ({columns_questions})
        '''
        cursor.execute(create_table_questions_sql)

        # Chèn dữ liệu từ DataFrame vào bảng
        for row in df_questions.itertuples(index=False):
            insert_sql = f'''
                INSERT INTO {questions_table} VALUES ({placeholders_questions})
            '''
            cursor.execute(insert_sql, tuple(row))

        conn.commit()
        print(f"Đã tạo và nhập dữ liệu vào bảng '{questions_table}' thành công.")
    except Exception as e:
        print(f"Lỗi khi xử lý sheet '{questions_sheet}': {e}")
        conn.rollback()

    # --- Đọc dữ liệu từ sheet 'Options' và tạo bảng 'options' ---
    try:
        df_options = pd.read_excel(excel_file, sheet_name=options_sheet)
        columns_options = ', '.join(df_options.columns)
        placeholders_options = ', '.join(['?'] * len(df_options.columns))
        create_table_options_sql = f'''
            CREATE TABLE IF NOT EXISTS {options_table} ({columns_options})
        '''
        cursor.execute(create_table_options_sql)

        for row in df_options.itertuples(index=False):
            insert_sql = f'''
                INSERT INTO {options_table} VALUES ({placeholders_options})
            '''
            cursor.execute(insert_sql, tuple(row))

        conn.commit()
        print(f"Đã tạo và nhập dữ liệu vào bảng '{options_table}' thành công.")
    except Exception as e:
        print(f"Lỗi khi xử lý sheet '{options_sheet}': {e}")
        conn.rollback()

    # Đóng kết nối
    conn.close()
    print("Đã đóng kết nối đến cơ sở dữ liệu.")

except Exception as e:
    print(f"Đã xảy ra lỗi tổng thể: {e}")
