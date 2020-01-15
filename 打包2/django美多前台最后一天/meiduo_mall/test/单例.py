# # class Single(object):
# #     def __new__(cls, *args, **kwargs):
# #         if not hasattr(cls, "_instance"):
# #             cls._instance = super(Single, cls).__new__(cls, *args, **kwargs)
# #         return cls._instance
# #
# # class A(Single):
# #     pass
# # a = A()
# # b = A()
#
#
#
# def dector(cls, *args, **kwargs):
#     def inner():
#         if not hasattr(cls, "_instance"):
#             cls._instance = cls(*args, **kwargs)
#         return cls._instance
#
#     return inner
#
#
# @dector
# class A(object):
#     pass
#
#
# a = A()
# b = A()
# print('a的id是：', id(a))
# print('b的id是：', id(b))
# def dector(cls,*args,**kwargs):
#     _instance={}
#     def inner():
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kwargs)
#         return _instance[cls]
#     return inner
# @dector
# class A(object):
#     pass
#
#
# a = A()
# b = A()
# print('a的id是：', id(a))
# print('b的id是：', id(b))