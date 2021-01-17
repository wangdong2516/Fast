1. 对路径参数的校验，使用Path
2. 对查询参数的校验，使用Query
3. 对请求体的校验，使用Body
4. 在Pydantic 模型内部声明校验和元数据，使用Field

以上进行数据校验和声明的方式是相同的，包括它们的参数等等也完全相同
   
请记住当你从 fastapi 导入 Query、Path 等对象时，他们实际上是返回特殊类的函数。

```python
def Query(  # noqa: N802
    default: Any,
    *,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    deprecated: Optional[bool] = None,
    **extra: Any,
) -> Any:
    pass
```

官方文档地址[https://fastapi.tiangolo.com/]