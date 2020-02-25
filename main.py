#!/usr/bin/env python
#  coding: cp1250

import wx
import re


def zamknij(evt):
    dialog = wx.MessageDialog(okno1, 'Czy na pewno?', 'Kończymy pracę', style=wx.OK | wx.CANCEL)
    x = dialog.ShowModal()
    dialog.Destroy()
    if x == wx.ID_OK:
        okno1.Close()


def otworz_fasta(evt):
    dialog = wx.FileDialog(okno1, message='Wybierz plik FASTA', defaultFile='', wildcard='*.FASTA', style=wx.FD_OPEN,
                           pos=(10, 10))
    if dialog.ShowModal() == wx.ID_OK:
        plik = dialog.GetPaths()
        plik_tekst = open(plik[0], 'r')
        odczyt = plik_tekst.read()
        odczyt = odczyt.splitlines()
        plik_tekst.close()
        sekwencje[:] = []
        nazwy[:] = []
        nazwa = ''
        for p in odczyt:
            if p[0] == '>':
                if nazwa != '':
                    sekwencje.append([gi, gb, sekw, nazwa])
                    nazwy.append(nazwa)
                pp = p.split('|')
                gi = pp[1]
                if len(pp) > 3:
                    gb = pp[3]
                    nazwa = pp[4]
                else:
                    gb = ""
                    nazwa = pp[2]
                sekw = ''
            else:
                sekw += p

        sekwencje.append([gi, gb, sekw, nazwa])
        nazwy.append(nazwa)
        lista.InsertItems(nazwy, 0)
        lista.Show()
        dialog.Destroy()


def otworz_genbank(evt):
    lista.Clear()
    tekst_organizm.Show()
    lista2.Hide()
    tekst_cds.Hide()
    tekst_ilosc.Hide()
    lista3.Hide()

    nazwaPattern = r'DEFINITION\s*(.*)ACCESSION'
    genePattern = r'/gene="(.*)"'
    proteinPattern = r'/protein_id="(.*)"'
    originPattern = r'([a-z])'
    translationPattern = r'/translation="([A-Z]*)"'
    dialog = wx.FileDialog(okno1, message='Wybierz plik GenBank', defaultFile='', wildcard='*.gb', style=wx.FD_OPEN,
                           pos=(10, 10))
    if dialog.ShowModal() == wx.ID_OK:
        plik = dialog.GetPaths()
        with open(plik[0]) as full:
            for line in full:
                if 'LOCUS' not in line:
                    continue
                else:
                    x = full.read()
                    out = (line + x)
                    out = out.strip('\n')

        odczyt_out = out.split('//\n')
        full.close()
        sekwencje[:] = []
        nazwy[:] = []
        for obiekt in odczyt_out:
            odczyt_origin = obiekt.split('ORIGIN')
            origin = odczyt_origin[1]
            seq = re.findall(originPattern, origin)

            nazywanie = obiekt.replace('\n', '').replace('            ', ' ')
            translacje = obiekt.replace('\n', '').replace(' ', '')

            nazwa = re.search(nazwaPattern, nazywanie)
            nazwy.append(nazwa[1])

            gen = re.findall(genePattern, obiekt)
            if gen == []:
                gen = re.findall(proteinPattern, obiekt)
            gen = list(dict.fromkeys(gen))

            translation = re.findall(translationPattern, translacje)
            sekwencje.append([nazwa[1], [gen, translation], seq])
    lista.InsertItems(nazwy, 0)
    lista.Show()
    dialog.Destroy()


def ile_nukleotydow(evt):
    lista3.Hide()
    tekst_ilosc.Hide()
    lista2.Clear()
    ktory = lista.GetSelection()
    lp = 'lp. ' + str(ktory)
    seq = sekwencje[ktory][2]

    if ('R' or 'D' or 'B' or 'Q' or 'E' or 'Z' or 'H' or 'I' or 'L' or 'K' or 'M' or 'F' or 'P' or 'S' or 'W' or 'Y' or 'V') in seq:
        rodzaj = 'Sekwencja aminokwasowa'
        liczba = 'Ilość aminokwasów: ' + str(len(seq))
    else:
        rodzaj = 'Sekwencja nukleotydowa'
        liczba = 'Ilość nukleotydów: ' + str(len(seq))

    wynik = [lp, rodzaj, liczba]
    lista2.InsertItems(wynik, 0)
    lista2.Show()


def ile_rodzajow(evt):
    lista3.Hide()
    tekst_ilosc.Hide()
    lista2.Clear()
    ktory = lista.GetSelection()
    lp = 'lp. ' + str(ktory)
    seq = sekwencje[ktory][2]

    if ('R' or 'D' or 'B' or 'Q' or 'E' or 'Z' or 'H' or 'I' or 'L' or 'K' or 'M' or 'F' or 'P' or 'S' or 'W' or 'Y' or 'V') in seq:
        rodzaj = 'Sekwencja aminokwasowa'
    else:
        rodzaj = 'Sekwencja nukleotydowa'

    wynik[:] = []
    literki[:] = []
    wynik.extend([lp, rodzaj])
    for i in seq:
        if literki.count(i) == 0:
            literki.append(i)
            liczba = seq.count(i)
            wynik.append(str.upper(i) + ': ' + str(liczba))

    lista2.InsertItems(wynik, 0)
    lista2.Show()


def ile_genow(evt):
    try:
        tekst_ilosc.Hide()
        tekst_cds.Show()
        lista3.Hide()
        lista2.Clear()
        ktory = lista.GetSelection()
        wynik = sekwencje[ktory][1][0]
        lista2.InsertItems(wynik, 0)
        lista2.Show()

    except AssertionError:
        wynik = ['BRAK CDS!!!']
        lista2.InsertItems(wynik, 0)
        lista2.Show()


def ile_cds(evt):
    tekst_ilosc.Show()
    lista3.Clear()
    ktory = lista.GetSelection()
    ktory_gen = lista2.GetSelection()
    seq = sekwencje[ktory][1][1][ktory_gen]

    wynik[:] = []
    literki[:] = []
    for i in seq:
        if literki.count(i) == 0:
            literki.append(i)
            liczba = seq.count(i)
            wynik.append(i + ': ' + str(liczba))

    lista3.InsertItems(wynik, 0)
    lista3.Show()


prog = wx.App()

sekwencje = []
nazwy = []
wynik = []
literki = []
okno1 = wx.Frame(None, title='Menu programu', size=(875, 500))

menuListwa = wx.MenuBar()
progMenu = wx.Menu()

progMenuItemA1 = progMenu.Append(wx.ID_ANY, 'Fasta', 'Czytaj Dane')
okno1.Bind(wx.EVT_MENU, otworz_fasta, progMenuItemA1)

progMenuItemA2 = progMenu.Append(wx.ID_ANY, 'GenBank', 'Czytaj Dane')
okno1.Bind(wx.EVT_MENU, otworz_genbank, progMenuItemA2)

menuListwa.Append(progMenu, 'Dane')

progMenu = wx.Menu()
progMenuItemB1 = progMenu.Append(wx.ID_ANY, 'Liczba cząsteczek', 'Oblicz1')
progMenuItemB2 = progMenu.Append(wx.ID_ANY, 'Liczba rodzajów', 'Oblicz2')
progMenuItemB3 = progMenu.Append(wx.ID_ANY, 'Geny', 'Oblicz3')

okno1.Bind(wx.EVT_MENU, ile_nukleotydow, progMenuItemB1)
okno1.Bind(wx.EVT_MENU, ile_rodzajow, progMenuItemB2)
okno1.Bind(wx.EVT_MENU, ile_genow, progMenuItemB3)

menuListwa.Append(progMenu, 'Obliczenia')

progMenu = wx.Menu()
progMenuItemC1 = progMenu.Append(wx.ID_EXIT, 'Koniec', 'Koniec programu')
menuListwa.Append(progMenu, 'Wyjście')
okno1.Bind(wx.EVT_MENU, zamknij, progMenuItemC1)

okno1.SetMenuBar(menuListwa)
panel = wx.Panel(parent=okno1, size=(875, 500))

tekst_organizm = wx.StaticText(panel, -1, 'Organizm:', (20, 7))
lista = wx.ListBox(panel, pos=(20, 30), size=(400, 390), style=wx.LB_HSCROLL)
tekst_organizm.Hide()

tekst_cds = wx.StaticText(panel, -1, 'CDS:', (440, 7))
lista2 = wx.ListBox(panel, pos=(440, 30), size=(320, 390))
lista2.Bind(wx.EVT_LISTBOX, ile_cds)
tekst_cds.Hide()

tekst_ilosc = wx.StaticText(panel, -1, 'Ilość:', (780, 7))
lista3 = wx.ListBox(panel, pos=(780, 30), size=(60, 390))
tekst_ilosc.Hide()


lista.Hide()
lista2.Hide()
lista3.Hide()
okno1.Center()
okno1.Show()
prog.MainLoop()
