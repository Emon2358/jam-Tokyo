from PIL import Image, ImageDraw, ImageFont

# 設定
IMAGE_PATH = "input.png"      # リポジトリ内の画像ファイル（必要に応じて変更）
OUTPUT_IMAGE = "ascii_art.png"  # 出力先PNGファイル名
NEW_WIDTH = 100               # ASCIIアートの横の文字数
FONT_PATH = "NotoSansCJK-Regular.ttc"  # 日本語対応フォントファイルのパス（リポジトリに配置してください）
FONT_SIZE = 16                # フォントサイズ

def get_ascii_char(pixel):
    """
    ピクセルの輝度値に応じた文字を返す関数
    輝度 240以上は白とみなし、何も描画しない（空文字）にする
    """
    if pixel >= 240:
        return " "   # 白：何も描画しない（空白）
    elif pixel >= 170:
        return "悲"
    elif pixel >= 85:
        return "無"
    else:
        return "鬱"

def main():
    # 画像の読み込み
    try:
        img = Image.open(IMAGE_PATH)
    except Exception as e:
        print(f"画像を開く際にエラーが発生しました: {e}")
        return

    # グレースケールに変換
    img = img.convert("L")

    # アスペクト比を保ちながらリサイズ（出力する文字数に合わせる）
    width, height = img.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * NEW_WIDTH * 0.5)  # 文字の縦横比を考慮した補正
    img = img.resize((NEW_WIDTH, new_height))

    # 各ピクセルを文字に変換してアスキーアート（文字列のリスト）を生成
    ascii_art_lines = []
    for y in range(new_height):
        line = ""
        for x in range(NEW_WIDTH):
            pixel = img.getpixel((x, y))
            line += get_ascii_char(pixel)
        ascii_art_lines.append(line)

    ascii_art = "\n".join(ascii_art_lines)
    print(ascii_art)

    # 描画用フォントの読み込み（日本語対応フォントを使用）
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except Exception as e:
        print(f"フォントの読み込みに失敗しました: {e}")
        font = ImageFont.load_default()

    # 各文字のサイズを取得
    # ※各文字は同じサイズ（等幅フォント前提）として計算
    char_width, char_height = font.getsize("鬱")

    # 描画する画像サイズを計算（文字数×フォントサイズ）
    image_width = char_width * NEW_WIDTH
    image_height = char_height * new_height

    # 白背景のキャンバスを生成
    canvas = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(canvas)

    # ASCIIアートを1行ずつ描画
    for i, line in enumerate(ascii_art_lines):
        draw.text((0, i * char_height), line, fill="black", font=font)

    # 結果をPNG画像として保存
    canvas.save(OUTPUT_IMAGE)
    print(f"ASCIIアート画像を {OUTPUT_IMAGE} として保存しました。")

if __name__ == "__main__":
    main()
