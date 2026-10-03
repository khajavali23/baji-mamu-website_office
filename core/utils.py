from .models import ActivityLog

def log(request,action,obj):
    if request.user.is_authenticated: ActivityLog.objects.create(user=request.user,action=action,object_type=obj.__class__.__name__,object_name=str(obj))

def crumbs(item):
    out=[]; seen=set(); cur=item
    while cur and cur.pk not in seen:
        out.append(cur); seen.add(cur.pk); cur=cur.parent
    return list(reversed(out))
