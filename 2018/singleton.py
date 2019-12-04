class Meta(type):
  def __call__(cls, key, *args, **kwarg):
    if not hasattr(cls, "items"):
      cls.items = {}
    if key in cls.items:
      return cls.items[key]
    o = super().__call__(key, *args, **kwarg)
    cls.items[key] = o
    return o
