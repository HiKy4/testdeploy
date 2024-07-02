from django.shortcuts import render
from django.http import JsonResponse
from .db_connect import collection, collectionCart
from django.http import HttpResponse
from prefixspan import PrefixSpan
from django.core.serializers.json import DjangoJSONEncoder
from bson import ObjectId
#products =[
#    ['A', 'B', 'C', 'A'],
#    ['A', 'D', 'B'],
#    ['B', 'C', 'A', 'A'],
#   ['A', 'C', 'A'],
#]
#product = ['D']
# Create your views here.
def index(request):
    return HttpResponse("Welcome to my Django API")
#lấy dữ liệu từ mongodb (từ db_connect.py)
def get_data_from_mongodb():
    cursor = collection.find()
    data = [doc['products'] for doc in cursor]  # Giả sử dữ liệu có trường 'products' trong mỗi document
    return data
# Hàm lấy dữ liệu sản phẩm trong giỏ hàng
def get_cart_data():
    cursor = collectionCart.find()
    data = [doc['product'] for doc in cursor]  # Giả sử dữ liệu có trường 'product' trong mỗi document
    return data

#thuật toán prefixspan
# Áp dụng thuật toán PrefixSpan để tính toán patterns từ dữ liệu
def apply_prefixspan(data):
    ps = PrefixSpan(data)
    num_patterns = len(data)  # Số lượng mẫu trong dữ liệu
    min_support = int(num_patterns * 0.5)  # Tính toán ngưỡng support là 50% của số lượng mẫu
    
    # Lấy tất cả các pattern phổ biến
    all_patterns = ps.frequent(min_support)
    sorted_patterns = sorted(all_patterns, key=lambda x: x[1], reverse=True)
    
    return sorted_patterns

# View để hiển thị các patterns đã tính toán
def show_patterns(request):
    try:
        # Lấy các patterns từ hàm apply_prefixspan
        data = get_data_from_mongodb()
        patterns = apply_prefixspan(data)  # Lấy patterns từ JSON response

        # Chuyển đổi patterns sang JSON để hiển thị
        return JsonResponse({'patterns': patterns}, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Hàm gợi ý sản phẩm dựa trên các mẫu phổ biến và giỏ hàng hiện tại
def recommend_products(current_cart, patterns):
    recommendations = []

    for support, pattern in patterns:
        # Kiểm tra xem mẫu có thỏa mãn điều kiện để đưa ra gợi ý không
        if len(pattern) > 1 and all(item in current_cart for item in pattern[:-1]) and pattern[-1] not in current_cart:
            recommendations.append(pattern[-1])

    # Loại bỏ các sản phẩm trùng lặp trong recommendations
    unique_recommendations = list(set(recommendations))
    unique_recommendations.sort()  # Sắp xếp các sản phẩm theo thứ tự từ điển (nếu cần)

    return unique_recommendations

# View để gợi ý các sản phẩm dựa trên lịch sử mua hàng và giỏ hàng hiện tại
def suggest_products(request):
    try:
        # Lấy dữ liệu lịch sử mua hàng và sản phẩm trong giỏ hàng từ MongoDB
        transaction_data = get_data_from_mongodb()
        cart_data = get_cart_data()
        
        # Áp dụng thuật toán PrefixSpan để tạo các mẫu phổ biến từ lịch sử mua hàng
        patterns = apply_prefixspan(transaction_data)
        
        # Gợi ý các sản phẩm dựa trên giỏ hàng hiện tại và các mẫu phổ biến
        recommended_products = recommend_products(cart_data, patterns)
        
        # Trả về kết quả gợi ý
        return JsonResponse({'recommended_products': recommended_products}, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

