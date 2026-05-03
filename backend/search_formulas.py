from database import SessionLocal
from app.models import FormulaEntry

def search_formulas(keyword: str):
    db = SessionLocal()
    try:
        # Tìm kiếm các công thức có chứa từ khóa trong latex_content
        # Sử dụng ilike để tìm kiếm không phân biệt hoa thường
        results = (
            db.query(FormulaEntry)
            .filter(FormulaEntry.latex_content.ilike(f"%{keyword}%"))
            .all()
        )

        print(f"\n--- KET QUA TIM KIEM VOI TU KHOA: '{keyword}' ---")
        if not results:
            print("Khong tim thay cong thuc nao.")
        else:
            print(f"{'ID':<38} | {'Noi dung LaTeX'}")
            print("-" * 80)
            for formula in results:
                print(f"{str(formula.id):<38} | {formula.latex_content}")
            print("-" * 80)
            print(f"Tim thay: {len(results)} ket qua.\n")
        
        return results

    except Exception as e:
        print(f"Co loi xay ra: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Chạy thử nghiệm với từ khóa "sqrt"
    search_formulas("sqrt")
