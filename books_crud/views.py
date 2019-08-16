from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth import logout
from django.shortcuts import redirect

from books_crud.models import Book


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'pages']


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def book_list(request, template_name='books_crud/book_list.html'):
    books = Book.objects.all()
    data = {'books': books}
    return render(request, template_name, data)


@login_required
def book_create(request, template_name='books_crud/book_form.html'):
    form = BookForm(request.POST or None)
    if form.is_valid():
        book = form.save(commit=False)
        book.user = request.user
        book.save()
        return redirect('books_crud:book_list')
    return render(request, template_name, {'form': form, 'type': 'Creating'})


@login_required
def book_update(request, pk, template_name='books_crud/book_form.html'):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('books_crud:book_list')
    return render(request, template_name, {'form':form, 'type': 'Updating'})


@login_required
def book_delete(request, pk, template_name='books_crud/book_confirm_delete.html'):
    book = get_object_or_404(Book, pk=pk)
    if request.method in ['POST']:
        book.delete()
        return redirect('books_crud:book_list')
    return render(request, template_name, {'object': book, 'type': 'Deleting'})
