# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
import json
import re
import xbmcvfs
import xbmc

from resources.lib.comaddon import progress, VSlog, dialog, addon
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, QuotePlus

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
headers = {'User-Agent': UA}

SITE_IDENTIFIER = 'extreme_down'
SITE_NAME = '[COLOR violet]Extreme Down[/COLOR]'
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent'

URL_MAIN = 'https://www.extreme-down.video/'

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0] + 'do=search&subaction=search&titleonly=3&speedsearch=1&story=', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + 'do=search&subaction=search&titleonly=3&speedsearch=2&story=', 'showMovies')
URL_SEARCH_ANIMES = (URL_SEARCH[0] + 'do=search&subaction=search&titleonly=3&speedsearch=4&story=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0] + 'do=search&subaction=search&titleonly=3&speedsearch=3&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuFilms')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_HD1080 = (URL_MAIN + 'films-new-hd/new-bluray-1080p/', 'showMovies')
# MOVIE_GENRES = (True, 'showGenres')
# MOVIE_ANNEES = (True, 'showMovieYears')

MOVIE_VOSTFR = (URL_MAIN + 'films-vostfr/dvdrip-vostfr', 'showMovies')
# MOVIE_4K = (URL_MAIN + 'films-new-ultrahd/', 'showMovies')
MOVIE_4K = (URL_MAIN + 'films-new-ultrahd/new-webrip-4k/', 'showMovies')
MOVIE_720 = (URL_MAIN + 'films-new-hd/new-bluray-720p/', 'showMovies')
MOVIE_1080X265 = (URL_MAIN + 'films-hd/films-1080p-x265', 'showMovies')
MOVIE_BLURAYVOSTFR = (URL_MAIN + 'films-vostfr/films-1080p-vostfr', 'showMovies')
MOVIE_3D = (URL_MAIN + 'films-new-hd/new-full-bluray-3d', 'showMovies')
MOVIE_FULL1080P = (URL_MAIN + 'films-new-hd/new-full-bluray', 'showMovies')
# MOVIE_FULL4K = (URL_MAIN + 'films-new-ultrahd/new-full-bluray-ultrahd-4k', 'showMovies')
MOVIE_FULL4K = (URL_MAIN + 'films-new-ultrahd/new-ultrahd-4k/', 'showMovies')
MOVIE_4KL = (URL_MAIN + 'films/ultrahd-4k/', 'showMovies')
MOVIE_LIGHT720 = (URL_MAIN + 'films-hdlight/hdlight-720p', 'showMovies')
MOVIE_LIGHT1080 = (URL_MAIN + 'films-hdlight/hdlight-1080p', 'showMovies')
MOVIE_LIGHTBDRIP = (URL_MAIN + 'films-new-hd/new-bdrip-720p', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films-sd/dvdrip', 'showMovies')
MOVIE_OLDDVD = (URL_MAIN + 'films-sd/ancien-dvdrip', 'showMovies')
MOVIE_FILMO = (URL_MAIN + 'films-sd/filmographie', 'showMovies')
MOVIE_CLASSIQUE_SD = (URL_MAIN + 'films-classique/classiques-sd', 'showMovies')
MOVIE_CLASSIQUE_HD = (URL_MAIN + 'films-classique/classiques-hd', 'showMovies')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_HD = (URL_MAIN + 'series-hd/1080p-series-vf', 'showMovies')
# SERIE_GENRES = (True, 'showGenres')
# SERIE_ANNEES = (True, 'showSerieYears')
SERIE_VOSTFRS = (URL_MAIN + 'series-hd/1080p-series-vostfr/', 'showMovies')
SERIE_720VO = (URL_MAIN + 'series-hd/hd-series-vostfr', 'showMovies')
SERIE_720VF = (URL_MAIN + 'series-hd/hd-series-vf', 'showMovies')
SERIE_4K = (URL_MAIN + 'series-hd/hd-x265-hevc/', 'showMovies')
SERIE_MULTI = (URL_MAIN + 'series-hd/hd-series-multi/', 'showMovies')
SERIE_SDVO = (URL_MAIN + 'series/vostfr/', 'showMovies')
SERIE_SDVF = (URL_MAIN + 'series/vf/', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showMovies')
ANIM_FILM = (URL_MAIN + 'mangas/manga-films/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'mangas/series-vostfr/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'mangas/series-vf/', 'showMovies')
ANIM_MULTI = (URL_MAIN + 'mangas/series-multi/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')
SPECTACLE_NEWS = (URL_MAIN + 'theatre/', 'showMovies')


def load():
    ADDON = addon()
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAutre', 'Autres', 'tv.png', oOutputParameterHandler)

    if ADDON.getSetting('token_alldebrid') == "":
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'getToken', '[COLOR red]Les utilisateurs d\'Alldebrid cliquez ici.[/COLOR]', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD1080[1], 'Bluray 1080P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Webrip 4K', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FULL4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FULL4K[1], 'Ultra HD 4KRemux', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4KL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4KL[1], 'Ultra HD 4KLight', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_720[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_720[1], 'Bluray 720P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1080X265[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1080X265[1], 'Bluray 1080P H265/HEVC', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BLURAYVOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BLURAYVOSTFR[1], 'Bluray VOSTFR', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Bluray 3D', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FULL1080P[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FULL1080P[1], 'REMUX 1080P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FULL4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FULL4K[1], 'REMUX 4K', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHT720[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHT720[1], 'HD light 720P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHT1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHT1080[1], 'HD light 1080P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHTBDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHTBDRIP[1], 'HD light BDRIP', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films BDRIP/DVDRIP', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_OLDDVD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_OLDDVD[1], 'Ancien DVDRIP', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FILMO[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FILMO[1], 'Filmographie', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIQUE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASSIQUE_HD[1], 'Films Classique HD', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIQUE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASSIQUE_SD[1], 'Films Classique SD', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'Séries 1080p VF', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries 1080p VOSTFR', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_720VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_720VF[1], 'Séries 720p VF', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_720VO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_720VO[1], 'Séries 720p VOSTFR', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_4K[1], 'Séries 4K H265/HEVC', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_MULTI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MULTI[1], 'Séries multilangue', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SDVF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SDVF[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SDVO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SDVO[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_FILM[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_FILM[1], "Film d'animation japonais (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], "Animés VOSTFR (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], "Animés VF (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MULTI[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MULTI[1], "Animés multilangue (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAutre():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Autres)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oOutputParameterHandler.addParameter('misc', True)
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], "Documentaire (Derniers ajouts)", 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECTACLE_NEWS[0])
    oOutputParameterHandler.addParameter('misc', True)
    oGui.addDir(SITE_IDENTIFIER, SPECTACLE_NEWS[1], "Spectacle et théatre (Derniers ajouts)", 'buzz.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getToken():
    ADDON = addon()
    oGui = cGui()

    token = oGui.showKeyBoard(heading="Entrez votre token")
    ADDON.setSetting('token_alldebrid', token)
    dialog().VSinfo('Token Ajouter', "Extreme-Download", 15)
    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl += sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'action/'])
    liste.append(['Animation', URL_MAIN + 'animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'arts-martiaux/'])
    liste.append(['Aventure', URL_MAIN + 'aventure/'])
    liste.append(['Biopic', URL_MAIN + 'biopic/'])
    liste.append(['Comédie', URL_MAIN + 'comedie/'])
    liste.append(['Comédie Dramatique', URL_MAIN + 'comedie-dramatique/'])
    liste.append(['Comédie Musicale', URL_MAIN + 'comedie-musicale/'])
    liste.append(['Documentaire', URL_MAIN + 'documentaire/'])
    liste.append(['Drame', URL_MAIN + 'drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'epouvante-horreur/'])
    liste.append(['Erotique', URL_MAIN + 'erotique'])
    liste.append(['Espionnage', URL_MAIN + 'espionnage/'])
    liste.append(['Famille', URL_MAIN + 'famille/'])
    liste.append(['Fantastique', URL_MAIN + 'fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'guerre/'])
    liste.append(['Historique', URL_MAIN + 'historique/'])
    liste.append(['Musical', URL_MAIN + 'musical/'])
    liste.append(['Policier', URL_MAIN + 'policier/'])
    liste.append(['Péplum', URL_MAIN + 'peplum/'])
    liste.append(['Romance', URL_MAIN + 'romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'science-fiction/'])
    liste.append(['Spectacle', URL_MAIN + 'spectacle/'])
    liste.append(['Thriller', URL_MAIN + 'thriller/'])
    liste.append(['Western', URL_MAIN + 'western/'])
    liste.append(['Divers', URL_MAIN + 'divers/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    for i in reversed(range(1913, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()

    for i in reversed(range(1936, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    nextPageSearch = oInputParameterHandler.getValue('nextPageSearch')
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMisc = oInputParameterHandler.getValue('misc') # Autre contenu

    if nextPageSearch:
        sSearch = siteUrl

    sCat = None
    if sSearch:
        siteUrl = sSearch

        if URL_SEARCH[0] in sSearch:
            sSearch = sSearch.replace(URL_SEARCH[0], '')
        

        if nextPageSearch:
            sSearch += '&search_start=' + nextPageSearch
        oRequestHandler = cRequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParametersLine(sSearch)
        oRequestHandler.addParameters('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = oParser.abParse(sHtmlContent, 'de la recherche', 'À propos')

        sCat = int(re.search('speedsearch=(\d)', sSearch).group(1))
        sSearch = re.search('story=(.+?)($|&)', sSearch).group(1)
    else:
        oRequestHandler = cRequestHandler(siteUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'class="top-last thumbnails" href="([^"]+)".+?"img-post" src="([^"]+).+?alt="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # on enleve les softwares
            if 'PC' in aEntry[2]:  # for the search
                continue

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if ' - ' in aEntry[2]:
                sTitle = aEntry[2].split(' - ')[0]
                sQual = aEntry[2].split(' - ')[1].replace('Avec TRUEFRENCH', '').replace('TRUEFRENCH', '').replace('FRENCH ', '')
                if 'Saison' in sQual:  # Pour les séries et animes
                    # * et non pas + car parfois "Saison integrale" pas de chiffre
                    saison = re.search('(Saison [0-9]*)', sQual).group(1)
                    sTitle = sTitle + ' ' + saison
                    sQual = re.sub('Saison [0-9]+ ', '', sQual)
            else:
                sTitle = aEntry[2]#.replace('Avec TRUEFRENCH', '').replace('TRUEFRENCH', '').replace('FRENCH ', '')
                sQual = ''

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            key = sTitle + "-" + sThumb
            if key in titles :
                continue
            titles.add(key)

            if sSearch and total > 5:
                if cUtil().CheckOccurence(sSearch, sTitle) == 0:
                    continue

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if sCat == 3 or sMisc:
                oGui.addMisc(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif sCat == 1 or '/films-' in siteUrl or '/manga-films/' in siteUrl :
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif sCat == 4 or '/mangas/' in siteUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if sSearch:
            sPattern = '<a name="nextlink" id="nextlink" onclick="javascript:list_submit\(([0-9]+)\); return\(false\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('misc', sMisc)
                oOutputParameterHandler.addParameter('nextPageSearch', aResult[1][0])
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oOutputParameterHandler.addParameter('misc', sMisc)
                number = re.search('/page/([0-9]+)', sNextPage).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

    if nextPageSearch:
        oGui.setEndOfDirectory()

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^"]+)">Suivant &.+?</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showMoviesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = '<blockquote.+?>([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = cUtil().removeHtmlTags(aResult[1][0])
    except:
        pass

    sPattern = '(<title>Télécharger |<title>)([^"]+) - ([^"]+)</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[1]):
        sMovieTitle = aResult[1][0][1]
        sQual = aResult[1][0][2].replace('"', '')

    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualités disponibles :[/COLOR]')

    sDisplayTitle = ('%s (%s)') % (sMovieTitle, sQual)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sPattern = '<a class="btn-other" href="([^<]+)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sQual = aEntry[1]
            sTitle = ('%s [%s]') % (sMovieTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sDisplayTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = '<blockquote.+?>([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = cUtil().removeHtmlTags(aResult[1][0])
    except:
        pass

    sPattern = '(<title>Télécharger |<title>)([^"]+) - ([^"]+)(VOSTFR|VF)*.+?</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)
    if (aResult[1]):
        sMovieTitle = aResult[1][0][1]

    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualités disponibles :[/COLOR]')

    sPattern = '<meta property="og:title" content=".+? - (.+?)(VOSTFR|VF)*/>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)

    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0][0].replace('"', '')
        if 'Saison' in sQual:  # N° de saison dans la qualite
            # * et non pas + car parfois "Saison integrale" pas de chiffre
            saison = re.search('(Saison [0-9]*)', sQual).group(1)
            sQual = re.sub('Saison [0-9]+ ', '', sQual)
            sMovieTitle = sMovieTitle + ' ' + saison

    sDisplayTitle = ('%s (%s)') % (sMovieTitle, sQual)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = '<a class="btn-other" href="([^"]+)">([^<]+)</a>'

    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if (aResult1[0] == True):
        for aEntry in aResult1[1]:
            sUrl = aEntry[0]
            sQual = aEntry[1]
            sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sHtmlContent2 = CutSais(sHtmlContent)
    sPattern2 = '<a class="btn-other" href="([^"]+)">([^<]+)<'

    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres saisons disponibles :[/COLOR]')

        for aEntry in aResult2[1]:

            sUrl = aEntry[0]
            sTitle = '[COLOR skyblue]' + aEntry[1] + '[/COLOR]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Detection de la taille des fichier pour separer les fichier premium des parties en .rar
    if not 'saison' in sUrl:
        fileSize = re.findall('<strong>Taille</strong><span style="float: right;">([^<]+)</span></td>', sHtmlContent)
        if 'et' in str(fileSize[0]):
            taille = str(fileSize[:-7])
        else:
            taille = str(fileSize[0])

        if ' Go' in taille:
            size, unite = taille.split(' ')
            if float(size) > 4.85:
                if "1 Lien" in sHtmlContent:
                    VSlog('1 Lien premium')
                    sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<div class="prez_2">1 Lien Uptobox</div>\s*.+?>\s*.+?<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<>]+)*</strong>.+?\s*<div class="showNFO"'
                else:
                    VSlog('Pas lien premium')
                    sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<>]+)* Premium</strong>'
            else:
                sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<>]+)*</strong>'
        else:
            sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<>]+)*</strong>'
    else:
        sPattern = '<div class="prez_7">([^<]+)</div>|<a title=".+?" href="([^"]+)" target="_blank"><strong class="hebergeur">([^<>]+)</strong>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    # Il n'existe que des fichiers en parties, non fonctionnel
    if (aResult[0] == False) and float(size) > 4.85:
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sUrl2 = aEntry[1]
                sTitle = sMovieTitle
                if 'saison' in sUrl:
                    sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, aEntry[2])
                else:
                    sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, str(aEntry[2]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addLink(SITE_IDENTIFIER, 'RecapchaBypass', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def RecapchaBypass():  # Ouverture de Chrome Launcher s'il est intallez
    ADDON = addon()
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    Token_Alldebrid = ADDON.getSetting('token_alldebrid')

    if Token_Alldebrid == "":
        RecapchaBypassOld(sUrl)
    else:
        sUrl_Bypass = "https://api.alldebrid.com/v4/link/redirector?agent=service&version=1.0-&apikey=" + Token_Alldebrid + "&link=" + sUrl

    oRequestHandler = cRequestHandler(sUrl_Bypass)
    sHtmlContent = json.loads(oRequestHandler.request())

    HostURL = sHtmlContent["data"]["links"]
    for sHosterUrl in HostURL:

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def RecapchaBypassOld(sUrl):  # Ouverture de Chrome Launcher s'il est intallez
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sPath = "special://home/addons/plugin.program.chrome.launcher/default.py"

    if xbmcvfs.exists(sPath):
        sUrl2 = QuotePlus(sUrl)
        xbmc.executebuiltin('RunPlugin("plugin://plugin.program.chrome.launcher/?url=' + sUrl2 + '&mode=showSite&stopPlayback=yes")')

    getHoster()


def getHoster():  # Ouvrir le clavier + requete
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    # appelle le clavier xbmc
    sSearchText = oGui.showKeyBoard(heading="Mettre le lien du hoster après avoir passer les Recaptchas manuellement")
    if (sSearchText != False):
        sUrl = sSearchText

        sHosterUrl = str(sUrl)
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="other-qualities">&Eacute;galement disponible en :</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    return ''


def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="other-qualities">Autres saisons :</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    return ''
