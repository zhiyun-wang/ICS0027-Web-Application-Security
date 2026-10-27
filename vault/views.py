import os

from cryptography.exceptions import InvalidTag
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .crypto import decrypt, encrypt
from .forms import EntryForm, RegisterForm, UnlockForm
from .models import Entry, VaultProfile


def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            user = form.save()

            VaultProfile.objects.create(
                user=user,
                salt=os.urandom(16)
            )

        messages.success(request, 'Account created. Please log in.')

        return redirect('login')

    return render(
        request,
        'vault/form.html',
        {
            'form': form,
            'title': 'Register'
        }
    )


@login_required
def entry_list(request):
    entries = Entry.objects.filter(
        owner=request.user
    ).order_by('website')

    return render(
        request,
        'vault/list.html',
        {'entries': entries}
    )


@login_required
@require_http_methods(['GET', 'POST'])
def entry_new(request):
    form = EntryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        master_password = data['master_password']

        if not request.user.check_password(master_password):
            form.add_error(
                'master_password',
                'Incorrect master password.'
            )

        else:
            nonce, ciphertext = encrypt(
                master_password,
                request.user.vaultprofile.salt,
                data['account_username'],
                data['account_password'],
                request.user.pk
            )

            Entry.objects.create(
                owner=request.user,
                website=data['website'],
                nonce=nonce,
                ciphertext=ciphertext
            )

            messages.success(request, 'Entry added.')

            return redirect('vault')

    return render(
        request,
        'vault/form.html',
        {
            'form': form,
            'title': 'Add entry'
        }
    )


@login_required
@require_http_methods(['GET', 'POST'])
def entry_detail(request, pk):
    entry = get_object_or_404(
        Entry,
        pk=pk,
        owner=request.user
    )

    form = UnlockForm(request.POST or None)
    values = None

    if request.method == 'POST' and form.is_valid():
        password = form.cleaned_data['master_password']

        if not request.user.check_password(password):
            form.add_error(
                'master_password',
                'Incorrect master password.'
            )

        else:
            try:
                values = decrypt(
                    password,
                    request.user.vaultprofile.salt,
                    entry.nonce,
                    entry.ciphertext,
                    request.user.pk
                )

            except (InvalidTag, ValueError):
                form.add_error(
                    None,
                    'Unable to decrypt this entry.'
                )

    return render(
        request,
        'vault/detail.html',
        {
            'entry': entry,
            'form': form,
            'values': values
        }
    )


@login_required
@require_http_methods(['GET', 'POST'])
def entry_edit(request, pk):
    entry = get_object_or_404(
        Entry,
        pk=pk,
        owner=request.user
    )

    form = EntryForm(
        request.POST or None,
        initial={'website': entry.website}
    )

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        master_password = data['master_password']

        if not request.user.check_password(master_password):
            form.add_error(
                'master_password',
                'Incorrect master password.'
            )

        else:
            nonce, ciphertext = encrypt(
                master_password,
                request.user.vaultprofile.salt,
                data['account_username'],
                data['account_password'],
                request.user.pk
            )

            entry.website = data['website']
            entry.nonce = nonce
            entry.ciphertext = ciphertext
            entry.save()

            messages.success(request, 'Entry updated.')

            return redirect('vault')

    return render(
        request,
        'vault/form.html',
        {
            'form': form,
            'title': 'Edit entry',
            'note': (
                'Enter the account username and password '
                'again when updating an entry.'
            )
        }
    )


@login_required
@require_http_methods(['GET', 'POST'])
def entry_delete(request, pk):
    entry = get_object_or_404(
        Entry,
        pk=pk,
        owner=request.user
    )

    if request.method == 'POST':
        entry.delete()

        messages.success(request, 'Entry deleted.')

        return redirect('vault')

    return render(
        request,
        'vault/delete.html',
        {'entry': entry}
    )