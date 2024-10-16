      getParadas(e) {        return e || (e = {}), this.http.get(`${s.uw}/superparadas/index.json`, {params: e}).pipe((0, i.U)(e => e.paradas));
      }      getParadasDestinoPorOrigen(e, t) {
        return t || (t = {}), this.http.get(`${s.uw}/superparadas/por-origen/${e = undefined !== e ? e : 0}.json`, {params: t}).pipe((0, i.U)(e => e));      }
      getExpedicionesPorOrigenYDestino(e, t, a, n) {        let r = {};
        return "limited" == n && (r = {collection: s.du}), this.http.get(`${s.uw}/buscador/search/${e}/${t}/${a}.json`, {params: r}).pipe((0, i.U)(e => e));      }
      getPrice(e, t, a) {        return this.http.get(`${s.uw}/buscador/precio/${e}/${t}.json`, {params: a});
      }      getLines() {
        return this.http.get(`${s.uw}/lineas/index.json`, {params: {collection: s.du, associated: "Expediciones.ParadaExpediciones.Paradas;Expediciones.ParadaOrigen;Expediciones.ParadaDestino;Expediciones.FrecuenciasSemanales;Expediciones.TemporadasAnuales;Expediciones.GescarPlanningHoy"}});      }
      getLine(e, t) {        return t || (t = {associated: "ParadasLineas.Paradas;Expediciones.ParadaExpediciones.Paradas;Expediciones.FrecuenciasSemanales;Expediciones.GescarPlanningHoy"}), this.http.get(`${s.uw}/lineas/view/${e}.json`, {params: t});
      }      getExpedition(e, t) {
        return t || (t = {}), this.http.get(`${s.uw}/expediciones/view/${e}.json`, {params: t}).pipe((0, i.U)(e => e));      }
      getStops(e) {        return e || (e = {}), this.http.get(`${s.uw}/superparadas/index.json`, {params: e}).pipe((0, i.U)(e => e));
      }      getStop(e) {
        return this.http.get(`${s.uw}/superparadas/view/${e}.json`).pipe((0, i.U)(e => e));      }
      getExpeditionsByStopToday(e) {        return this.http.get(`${s.uw}/superparadas/expediciones-fecha/${e}.json`).pipe((0, i.U)(e => e));
      }      getBusLastStop(e) {
        return this.http.get(`${s.uw}/buses/getLastStop/${e}.json`);      }
      getBusLastArea(e, t) {        return t || (t = {}), this.http.get(`${s.uw}/buses/getLastArea/${e}.json`, {params: t});
      }      getBusesGeolocs() {
        return this.http.get(`${s.uw}/buses/getGeolocs.json`, {params: {collection: s.du}});      }
      getBusGeoloc(e) {        return this.http.get(`${s.uw}/buses/getGeoloc/${e}.json`);
      }      getComunicaciones() {
        return this.http.get(`${s.bW}/comunicaciones/index.json`);      }
      getComunicacion(e) {        return this.http.get(`${s.bW}/comunicaciones/view/${e}.json`);
      }    }
    return e.ɵfac = function (t) {      return new (t || e)(n.LFG(r.eN));
    }, e.ɵprov = n.Yz7({token: e, factory: e.ɵfac, providedIn: "root"}), e;  })();
