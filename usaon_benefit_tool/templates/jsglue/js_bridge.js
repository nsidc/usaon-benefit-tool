{# Provide `{{namespace}}.url_for` JS function (default `Flask.url_for()`).

Vendored from https://github.com/stewartpark/Flask-JSGlue; appears abandoned.
Applied changes to work with modern versions of these dependencies.

Copyright 2022 Stewart Park
License: BSD 3-clause

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#}
var {{ namespace }} = new(function () {
  'use strict';
  return {
    '_endpoints': {{ rules|safe }},
    'url_for': function (endpoint, rule) {
      if (typeof rule === "undefined") rule = {};
      else if (typeof(rule) !== "object") {
        // rule *must* be an Object, anything else is wrong
        throw {name: "ValueError", message: "type for 'rule' must be Object, got: " + typeof(rule)};
      }

      var has_everything = false,
        url = "";

      var is_absolute = false,
        has_anchor = false,
        has_scheme;
      var anchor = "",
        scheme = "";

      if (rule['_external'] === true) {
        is_absolute = true;
        scheme = location.protocol.split(':')[0];
        delete rule['_external'];
      }

      if ('_scheme' in rule) {
        if (is_absolute) {
          scheme = rule['_scheme'];
          delete rule['_scheme'];
        } else {
          throw {
            name: "ValueError",
            message: "_scheme is set without _external."
          };
        }
      }

      if ('_anchor' in rule) {
        has_anchor = true;
        anchor = rule['_anchor'];
        delete rule['_anchor'];
      }

      for (var i in this._endpoints) {
        if (endpoint == this._endpoints[i][0]) {
          var url = '';
          var j = 0;
          var has_everything = true;
          var used = {};
          for (var j = 0; j < this._endpoints[i][2].length; j++) {
            var t = rule[this._endpoints[i][2][j]];
            if (typeof t === "undefined") {
              has_everything = false;
              break;
            }
            url += this._endpoints[i][1][j] + t;
            used[this._endpoints[i][2][j]] = true;
          }
          if (has_everything) {
            if (this._endpoints[i][2].length != this._endpoints[i][1].length)
              url += this._endpoints[i][1][j];

            var first = true;
            for (var r in rule) {
              if (r[0] != '_' && !(r in used)) {
                if (first) {
                  url += '?';
                  first = false;
                } else {
                  url += '&';
                }
                url += r + '=' + rule[r];
              }
            }
            if (has_anchor) {
              url += "#" + anchor;
            }

            if (is_absolute) {
              return scheme + "://" + location.host + url;
            } else {
              return url;
            }
          }
        }
      }

      throw {
        name: 'BuildError',
        message: "Endpoint '" + endpoint + "' does not exist or you have passed incorrect parameters " + JSON.stringify(rule)
      };
    }
  };
});
